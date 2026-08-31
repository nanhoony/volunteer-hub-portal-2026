import os
import sys
import csv
from collections import defaultdict

def main():
    input_file = "모집공고.csv"
    output_dir = "출력_분야별"
    summary_file = "결과_분야집계.csv"
    
    if not os.path.exists(input_file):
        print(f"오류: 입력 파일 '{input_file}'을 찾을 수 없습니다.")
        return
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 파싱 및 분야별 그룹화
    field_rows = defaultdict(list)
    field_summary = defaultdict(lambda: {"count": 0, "total_people": 0})
    
    # 인코딩 확인 (utf-8-sig 또는 utf-8)
    encoding = "utf-8"
    try:
        with open(input_file, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                field = row.get("분야", "").strip()
                if not field:
                    continue
                field_rows[field].append(row)
                
                # 모집인원 파싱
                try:
                    people = int(row.get("모집인원", 0))
                except (ValueError, TypeError):
                    people = 0
                
                field_summary[field]["count"] += 1
                field_summary[field]["total_people"] += people
    except UnicodeDecodeError:
        with open(input_file, mode="r", encoding="cp949") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                field = row.get("분야", "").strip()
                if not field:
                    continue
                field_rows[field].append(row)
                try:
                    people = int(row.get("모집인원", 0))
                except (ValueError, TypeError):
                    people = 0
                field_summary[field]["count"] += 1
                field_summary[field]["total_people"] += people

    # 1. 분야별 CSV 파일 저장
    for field, rows in field_rows.items():
        field_file_path = os.path.join(output_dir, f"{field}.csv")
        with open(field_file_path, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    
    # 2. 결과_분야집계.csv 저장
    # 컬럼: 분야,건수,총모집인원
    summary_headers = ["분야", "건수", "총모집인원"]
    sorted_fields = sorted(field_summary.keys())
    
    with open(summary_file, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(summary_headers)
        for field in sorted_fields:
            cnt = field_summary[field]["count"]
            tot = field_summary[field]["total_people"]
            writer.writerow([field, cnt, tot])
            
    # 3. 콘솔 출력
    print("=" * 45)
    print("        [ 자원봉사 모집공고 분야별 집계 ]")
    print("=" * 45)
    total_all_count = 0
    total_all_people = 0
    for field in sorted_fields:
        cnt = field_summary[field]["count"]
        tot = field_summary[field]["total_people"]
        total_all_count += cnt
        total_all_people += tot
        print(f"- {field}: {cnt}건 / 총 모집인원 {tot}명")
    print("-" * 45)
    print(f"총 합계: {len(sorted_fields)}개 분야 | {total_all_count}건 | 총 {total_all_people}명")
    print("=" * 45)
    print(f"[완료] 분야별 CSV 파일 분리 완료: '{output_dir}/' 폴더 ({len(field_rows)}개 파일)")
    print(f"[완료] 집계표 저장 완료: '{summary_file}'")

if __name__ == "__main__":
    # Windows 콘솔 인코딩 대응
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    main()
