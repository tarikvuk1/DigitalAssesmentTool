def generate_recommendations(row):
    recommendations = []

    infra = row.get("infrastructure_score", 0)
    process = row.get("process_score", 0)
    marketing = row.get("marketing_score", 0)
    overall = row.get("overall_score", 0)

    if infra < 0.5:
        recommendations.append(
            "Enhance core digital infrastructure by ensuring reliable internet connectivity, professional email systems, and a functional company website."
        )

    if process < 0.5:
        recommendations.append(
            "Digitize and streamline key business processes, including invoicing, order management, and internal data workflows."
        )

    if marketing < 0.5:
        recommendations.append(
            "Improve digital marketing capabilities by leveraging analytics tools, managing online reputation, and increasing social media engagement."
        )

    if overall < 0.5:
        recommendations.append(
            "Develop and implement a structured digital transformation strategy for the next 6–12 months with clear priorities and milestones."
        )

    if overall >= 0.75:
        recommendations.append(
            "Focus on continuous improvement, advanced analytics, and innovation to maintain competitive advantage."
        )

    if not recommendations:
        recommendations.append(
            "The company demonstrates a solid level of digital maturity. Continue optimizing existing systems and exploring innovation opportunities."
        )

    return " | ".join(recommendations)


def generate_roadmap(row):
    short_term = []
    mid_term = []
    long_term = []

    infra = row.get("infrastructure_score", 0)
    process = row.get("process_score", 0)
    marketing = row.get("marketing_score", 0)
    overall = row.get("overall_score", 0)

    if infra < 0.5:
        short_term.append("Set up essential digital infrastructure (internet, email, basic IT tools).")
        mid_term.append("Upgrade systems and introduce cloud-based collaboration tools.")
        long_term.append("Integrate scalable and secure infrastructure to support growth.")

    if process < 0.5:
        short_term.append("Implement basic digital tools for invoicing and order processing.")
        mid_term.append("Integrate processes into a centralized management system (ERP/CRM).")
        long_term.append("Automate workflows and enable real-time reporting and analytics.")

    if marketing < 0.5:
        short_term.append("Create a basic online presence (website and social media).")
        mid_term.append("Adopt analytics tools and actively manage online reputation.")
        long_term.append("Implement data-driven marketing strategies and customer segmentation.")

    if overall >= 0.75:
        short_term.append("Maintain current digital systems and monitor performance.")
        mid_term.append("Optimize customer experience and internal efficiency.")
        long_term.append("Invest in innovation, automation, and advanced digital business models.")

    return {
        "short_term": " | ".join(short_term) if short_term else "No short-term actions defined.",
        "mid_term": " | ".join(mid_term) if mid_term else "No mid-term actions defined.",
        "long_term": " | ".join(long_term) if long_term else "No long-term actions defined.",
    }