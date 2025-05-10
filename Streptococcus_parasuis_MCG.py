import os
import tempfile
import shutil
import subprocess
import argparse
import re

def main(query_genome, prefix):
    tempdir = tempfile.mkdtemp()

    refer_genome = os.path.join(os.path.dirname(__file__), "data", "BS26.fasta")
    refer_table = os.path.join(os.path.dirname(__file__), "data", "snps.table")

    # 运行 nucmer 和 dnadiff
    subprocess.run(["nucmer", query_genome, refer_genome, '-p', os.path.join(tempdir, prefix)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["dnadiff", '-d', f"{os.path.join(tempdir, prefix)}.delta", '-p', os.path.join(tempdir, prefix)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 解析 .snps 文件
    snp_file = os.path.join(tempdir, prefix) + ".snps"
    snp = {}
    with open(snp_file, 'r') as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) > 3 and parts[2] in "ATCGatcg":
                key = parts[-1] + "_" + parts[3]
                snp[key] = snp.get(key, 0) + 1

    # 处理 SNP 列表文件
    all_snps = {}
    group_snps = {}
    with open(refer_table) as f:
        for line in f:
            parts = line.strip().split("\t")
            all_snps[parts[0]] = all_snps.get(parts[0], 0) + 1
            key = parts[1] + "_" + parts[2]
            if key in snp:
                group_snps[parts[0]] = group_snps.get(parts[0], 0) + 1

    # 计算并输出结果到 YAML 文件
    results = {}
    max_value = -1
    final_cgt_key = ""
    for key in sorted(all_snps.keys()):
        value = group_snps.get(key, 0)

        if key == '2':  # Special case for CGT9
            value = 450 - value

        percentage = (value / all_snps[key]) * 100 if all_snps[key] else 0
        results[key] = round(percentage, 2)
        if percentage > max_value:
            max_value = percentage
            final_cgt_key = f"CGT {key}"

    # Write to YAML file
    output_file = prefix + ".yaml"
    with open(output_file, 'w') as out:
        for key, value in results.items():
            out.write(f"CGT {key} : {value}%\n")
        out.write(f"Final CGT : {final_cgt_key}\n")

    # 重新读取生成的 YAML 文件并更新 Final CGT 行
    updated_lines = []
    final_cgt_percentage = None

    with open(output_file, 'r') as infile:
        lines = infile.readlines()
        for line in lines[:-1]:  # 写入所有非最后一行
            updated_lines.append(line)
        
        # 查找 final_cgt_key 对应的百分比
        for line in lines:
            match = re.search(rf'^{re.escape(final_cgt_key)} : ([\d.]+)%$', line)
            if match:
                final_cgt_percentage = match.group(1)
                break

        # 获取最后一行的 Final CGT
        last_line = lines[-1].strip()
        final_cgt_match = re.search(r'Final CGT : (.+)', last_line)
        if final_cgt_match:
            final_cgt_name = final_cgt_match.group(1)
            # 将 - 及其后面的数字替换为空
            final_cgt_name_cleaned = re.sub(r'-\d+', '', final_cgt_name).strip()
            if final_cgt_percentage is not None:
                updated_lines.append(f"Final CGT : {final_cgt_name_cleaned} ({final_cgt_percentage}%)\n")
            else:
                updated_lines.append(f"Final CGT : {final_cgt_name_cleaned}\n")
        else:
            updated_lines.append(last_line + "\n")

    # 将更新后的行写回文件
    with open(output_file, 'w') as outfile:
        outfile.writelines(updated_lines)

    shutil.rmtree(tempdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster type")
    parser.add_argument("--genome", type=str, help="Genome file")
    parser.add_argument("--prefix", type=str, help="Prefix")
    args = parser.parse_args()

    main(args.genome, args.prefix)
