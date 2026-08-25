"""Command-Line Interface (CLI) for AI Resume Reviewer
Task ID: AI-SS-004 | Data Alcott Systems | Yash Malik (DAS005423)
"""

import argparse
import json
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from app.analyzer import ResumeReviewer


def print_banner():
    banner = """
======================================================================
  [AI RESUME REVIEWER] NLP & ML Analysis Engine
  Task ID: AI-SS-004 | Student Code: DAS005423 | Data Alcott Systems
======================================================================
"""
    print(banner)


def display_results(result: dict):
    scoring = result["scoring"]
    skills = result["skills"]
    exp = result["experience"]
    edu = result["education"]
    ats = result["ats_compatibility"]
    feedback = result["feedback"]
    jd = result["job_match"]

    print("\n" + "=" * 65)
    print(f"  OVERALL RESUME SCORE: {scoring['total_score']} / 100  [{scoring['letter_grade']}]")
    print("=" * 65)

    print("\n[+] Category Breakdown:")
    for cat_name, cat_data in scoring["categories"].items():
        score_val = cat_data["score"]
        max_val = cat_data["max"]
        bar_len = int((score_val / max_val) * 20)
        bar = "#" * bar_len + "-" * (20 - bar_len)
        print(f"  * {cat_name.replace('_', ' ').title():<22} [{bar}] {score_val:>4.1f} / {max_val} pts")

    print("\n[+] Technical Skills Detected ({} found):".format(skills["technical_count"]))
    for cat, items in skills["categorized_technical"].items():
        if items:
            print(f"  - {cat.replace('_', ' ').title()}: {', '.join(items)}")

    print(f"\n[+] Soft Skills: {', '.join(skills['soft_skills']) if skills['soft_skills'] else 'None detected'}")

    print("\n[+] Experience & Impact:")
    print(f"  * Estimated Tenure : ~{exp['years']} Years ({exp['seniority_level']})")
    print(f"  * Strong Verbs     : {exp['action_verbs']['strong_verbs_count']} detected ({', '.join(exp['action_verbs']['strong_verbs'][:5])})")
    print(f"  * Quantified Impact: {exp['metrics_count']} metrics ({', '.join(exp['quantified_metrics'][:3]) if exp['quantified_metrics'] else 'None detected'})")

    print("\n[+] Education:")
    print(f"  * Level: {edu['highest_degree_level'].replace('_', ' ').title()}")
    if edu["majors_found"]:
        print(f"  * Major(s): {', '.join(edu['majors_found'])}")
    if edu["institutions_found"]:
        print(f"  * Institution(s): {', '.join(edu['institutions_found'])}")

    print("\n[+] ATS Compatibility:")
    print(f"  * ATS Score : {ats['ats_score']} / 100 ({ats['status']})")
    email_status = "[YES]" if ats['contact_info']['has_email'] else "[NO]"
    phone_status = "[YES]" if ats['contact_info']['has_phone'] else "[NO]"
    li_status = "[YES]" if ats['contact_info']['has_linkedin'] else "[NO]"
    print(f"  * Contact   : Email: {email_status} | Phone: {phone_status} | LinkedIn: {li_status}")

    if jd and jd.get("is_active"):
        print("\n[+] Job Description Match Alignment:")
        print(f"  * Match Score   : {jd['match_score']}% ({jd['match_level']})")
        print(f"  * Matched Terms : {', '.join(jd['matched_keywords'][:8])}")
        print(f"  * Missing Terms : {', '.join(jd['missing_keywords'][:8])}")

    print("\n[+] Key Strengths:")
    for s in feedback["strengths"]:
        print(f"  [+] {s}")

    print("\n[!] Areas for Improvement:")
    for imp in feedback["areas_for_improvement"]:
        print(f"  [-] {imp}")

    if feedback["ats_recommendations"]:
        print("\n[*] ATS Optimization Tips:")
        for tip in feedback["ats_recommendations"]:
            print(f"  [*] {tip}")

    print("\n[>] Top 3 Next Action Steps:")
    for idx, step in enumerate(feedback["prioritized_next_steps"], 1):
        print(f"  {idx}. {step}")
    print("=" * 65 + "\n")


def main():
    parser = argparse.ArgumentParser(description="AI Resume Reviewer CLI Engine (Task AI-SS-004)")
    parser.add_argument("--resume", "-r", type=str, help="Path to resume file (PDF, DOCX, TXT)")
    parser.add_argument("--jd", "-j", type=str, default="", help="Target Job Description text string")
    parser.add_argument("--jd-file", type=str, default="", help="Path to text file containing Job Description")
    parser.add_argument("--batch-dir", "-b", type=str, help="Directory containing multiple resumes for batch analysis")
    parser.add_argument("--output", "-o", type=str, help="Path to export results as JSON")
    parser.add_argument("--sample", action="store_true", help="Run quick demo using built-in sample resume")

    args = parser.parse_args()
    print_banner()

    reviewer = ResumeReviewer()

    jd_text = args.jd
    if args.jd_file and os.path.exists(args.jd_file):
        with open(args.jd_file, "r", encoding="utf-8", errors="ignore") as f:
            jd_text = f.read()

    # Mode 1: Batch directory
    if args.batch_dir:
        if not os.path.isdir(args.batch_dir):
            print(f"[-] Error: Directory '{args.batch_dir}' does not exist.")
            sys.exit(1)

        files = [
            os.path.join(args.batch_dir, f)
            for f in os.listdir(args.batch_dir)
            if f.lower().endswith((".txt", ".pdf", ".docx"))
        ]
        if not files:
            print(f"[-] No valid resumes found in '{args.batch_dir}'.")
            sys.exit(1)

        print(f"[*] Analyzing {len(files)} resumes in batch mode...\n")
        all_results = []
        for file_path in files:
            print(f"--> Processing: {os.path.basename(file_path)}...")
            res = reviewer.analyze_resume(file_path, job_description=jd_text, filename=os.path.basename(file_path))
            all_results.append({
                "filename": os.path.basename(file_path),
                "score": res["scoring"]["total_score"],
                "grade": res["scoring"]["letter_grade"],
                "ats_score": res["ats_compatibility"]["ats_score"],
                "skills_count": res["skills"]["technical_count"],
                "experience_years": res["experience"]["years"]
            })

        print("\n" + "=" * 75)
        print("  BATCH EVALUATION SUMMARY TABLE")
        print("=" * 75)
        print(f"{'Filename':<35} {'Score':<10} {'Grade':<12} {'ATS':<10} {'Skills':<8}")
        print("-" * 75)
        for row in all_results:
            print(f"{row['filename'][:34]:<35} {row['score']:<10} {row['grade'][:11]:<12} {row['ats_score']:<10} {row['skills_count']:<8}")
        print("-" * 75)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as out_f:
                json.dump(all_results, out_f, indent=2)
            print(f"\n[+] Batch summary exported to: {args.output}")
        return

    # Mode 2: Sample Demo
    if args.sample or not args.resume:
        sample_path = os.path.join(
            os.path.dirname(__file__), "sample_resumes", "software_engineer_senior.txt"
        )
        if os.path.exists(sample_path):
            print("[*] Running analysis on sample Senior Software Engineer resume...")
            result = reviewer.analyze_resume(sample_path, job_description=jd_text)
            display_results(result)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as out_f:
                    json.dump(result, out_f, indent=2)
                print(f"[+] Full analysis exported to: {args.output}")
        else:
            print("[-] Please specify a resume file using --resume <file_path>")
        return

    # Mode 3: Single Resume Analysis
    if not os.path.exists(args.resume):
        print(f"[-] Error: Resume file '{args.resume}' does not exist.")
        sys.exit(1)

    print(f"[*] Analyzing resume: {args.resume}...")
    result = reviewer.analyze_resume(
        args.resume,
        job_description=jd_text,
        filename=os.path.basename(args.resume)
    )
    display_results(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, indent=2)
        print(f"[+] Analysis exported to: {args.output}")


if __name__ == "__main__":
    main()

