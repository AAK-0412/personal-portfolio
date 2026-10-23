
from backend.database import get_connection, create_tables, DATABASE_URL


projects = [
    {
        "title": "Enterprise Network Infrastructure",
        "description": (
            "Enterprise network infrastructure built with GNS3 and "
            "Wireshark, covering VLANs, DHCP, OSPF, NAT/PAT, ACLs, "
            "routing, and packet analysis."
        ),
        "technologies": "GNS3, Wireshark, OSPF, VLANs",
        "github_url": (
            "https://github.com/AAK-0412/"
            "enterprise-network-infrastructure"
        ),
        "demo_url": None,
        "status": "GitHub",
    },
    {
        "title": "Enterprise WAN & IPsec VPN",
        "description": (
            "Enterprise WAN infrastructure involving eBGP routing "
            "and site-to-site IPsec VPN using IKEv1, PFS, ESP, "
            "and Wireshark analysis."
        ),
        "technologies": "eBGP, IPsec, IKEv1, Wireshark",
        "github_url": (
            "https://github.com/AAK-0412/"
            "enterprise-wan-ipsec-vpn"
        ),
        "demo_url": None,
        "status": "GitHub",
    },
    {
        "title": "Password Strength Analyzer",
        "description": (
            "A Python tool for checking password strength and "
            "generating custom wordlists for ethical hacking "
            "and cybersecurity practice."
        ),
        "technologies": "Python, Cybersecurity, Password Analysis",
        "github_url": (
            "https://github.com/AAK-0412/"
            "password-strength-analyzer"
        ),
        "demo_url": None,
        "status": "GitHub",
    },
    {
        "title": "Stock Market Portfolio Analyzer",
        "description": (
            "A Python application for analyzing and comparing stock "
            "performance using Yahoo Finance data, portfolio statistics, "
            "customizable time ranges, and stock trend comparisons."
        ),
        "technologies": "Python, Yahoo Finance, Data Analysis",
        "github_url": (
            "https://github.com/AAK-0412/"
            "stock-market-portfolio-analyzer"
        ),
        "demo_url": None,
        "status": "GitHub",
    },
    {
        "title": "Personal Task Manager",
        "description": (
            "A full-stack task management application built with "
            "FastAPI and SQLite, supporting task creation, editing, "
            "completion tracking, filtering, and deletion."
        ),
        "technologies": "Python, FastAPI, SQLite, JavaScript",
        "github_url": None,
        "demo_url": None,
        "status": "Built Locally",
    },
]


def seed_projects():
    create_tables()
    connection = get_connection()

    # Use the correct placeholder style for each database.
    placeholder = "%s" if DATABASE_URL else "?"

    try:
        for project in projects:
            existing = connection.execute(
                f"SELECT id FROM projects WHERE title = {placeholder}",
                (project["title"],),
            ).fetchone()

            if existing:
                continue

            connection.execute(
                f"""
                INSERT INTO projects (
                    title,
                    description,
                    technologies,
                    github_url,
                    demo_url,
                    status
                )
                VALUES (
                    {placeholder},
                    {placeholder},
                    {placeholder},
                    {placeholder},
                    {placeholder},
                    {placeholder}
                )
                """,
                (
                    project["title"],
                    project["description"],
                    project["technologies"],
                    project["github_url"],
                    project["demo_url"],
                    project["status"],
                ),
            )

        connection.commit()
        print("Project database initialized successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_projects()

