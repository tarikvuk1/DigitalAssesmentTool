from loader import load_data
from cleaner import clean_column_names, rename_key_columns
from scorer import apply_basic_scoring, calculate_category_scores, get_maturity_level
from recommender import generate_recommendations, generate_roadmap


def main():
    file_path = "data/Test digitalne konkurentnosti.xlsx"
    df = load_data(file_path)

    df = clean_column_names(df)
    df = rename_key_columns(df)
    df = apply_basic_scoring(df)
    df = calculate_category_scores(df)

    if "overall_score" in df.columns:
        df["maturity_level"] = df["overall_score"].apply(get_maturity_level)
        df["recommendations"] = df.apply(generate_recommendations, axis=1)
        roadmaps = df.apply(generate_roadmap, axis=1)

        df["short_term_roadmap"] = roadmaps.apply(lambda x: x["short_term"])
        df["mid_term_roadmap"] = roadmaps.apply(lambda x: x["mid_term"])
        df["long_term_roadmap"] = roadmaps.apply(lambda x: x["long_term"])

    print("✅ REZULTATI:\n")

    result_cols = [
        col for col in [
            "company_name",
            "infrastructure_score",
            "process_score",
            "marketing_score",
            "hr_score",
            "innovation_score",
            "security_score",
            "overall_score",
            "maturity_level",
            "recommendations",
            "short_term_roadmap",
            "mid_term_roadmap",
            "long_term_roadmap",
        ] if col in df.columns
    ]

    print(df[result_cols].head())

    df.to_excel("data/rezultati_digitalne_zrelosti.xlsx", index=False)
    print("\n✅ Rezultati sačuvani u fajl: data/rezultati_digitalne_zrelosti.xlsx")


if __name__ == "__main__":
    main()