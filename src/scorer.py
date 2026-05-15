import pandas as pd
from cleaner import map_yes_no


def apply_basic_scoring(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    columns_to_score = [
        "internet_access",
        "business_email",
        "electronic_ordering",
        "receive_e_invoices",
        "process_e_invoices",
        "digital_data_flow",
        "digital_recruitment",
        "digital_investment_plan",
        "it_security_measures",
        "gdpr_compliance",
        "collaboration_tools",
        "has_website",
        "online_reputation",
        "website_analytics",
        "customer_loyalty",
        "social_media_campaigns",
        "customer_segmentation",
    ]

    for col in columns_to_score:
        if col in df.columns:
            df[col + "_score"] = df[col].apply(map_yes_no)

    return df


def calculate_category_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    infra_cols = [
        "internet_access_score",
        "business_email_score",
        "has_website_score",
    ]

    process_cols = [
        "electronic_ordering_score",
        "process_e_invoices_score",
        "digital_data_flow_score",
    ]

    marketing_cols = [
        "online_reputation_score",
        "website_analytics_score",
        "social_media_campaigns_score",
        "customer_segmentation_score",
    ]

    hr_cols = [
        "digital_recruitment_score",
    ]

    innovation_cols = [
        "digital_investment_plan_score",
    ]

    security_cols = [
        "it_security_measures_score",
        "gdpr_compliance_score",
    ]

    existing_infra = [col for col in infra_cols if col in df.columns]
    existing_process = [col for col in process_cols if col in df.columns]
    existing_marketing = [col for col in marketing_cols if col in df.columns]
    existing_hr = [col for col in hr_cols if col in df.columns]
    existing_innovation = [col for col in innovation_cols if col in df.columns]
    existing_security = [col for col in security_cols if col in df.columns]

    if existing_infra:
        df["infrastructure_score"] = df[existing_infra].mean(axis=1)

    if existing_process:
        df["process_score"] = df[existing_process].mean(axis=1)

    if existing_marketing:
        df["marketing_score"] = df[existing_marketing].mean(axis=1)

    if existing_hr:
        df["hr_score"] = df[existing_hr].mean(axis=1)

    if existing_innovation:
        df["innovation_score"] = df[existing_innovation].mean(axis=1)

    if existing_security:
        df["security_score"] = df[existing_security].mean(axis=1)

    weights = {
        "infrastructure_score": 0.25,
        "process_score": 0.25,
        "marketing_score": 0.15,
        "hr_score": 0.10,
        "innovation_score": 0.15,
        "security_score": 0.10,
    }

    score_cols = [col for col in weights.keys() if col in df.columns]

    if score_cols:
        df["overall_score"] = sum(
            df[col] * weights[col] for col in score_cols
        ) / sum(weights[col] for col in score_cols)

    return df


def get_maturity_level(score):
    if pd.isna(score):
        return "Unknown"
    elif score < 0.25:
        return "Beginner"
    elif score < 0.5:
        return "Basic"
    elif score < 0.75:
        return "Intermediate"
    else:
        return "Advanced"