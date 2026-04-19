import os
from dotenv import load_dotenv
from github import Github, Auth
from github.GithubException import GithubException
import re
import os


from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.theme import Theme
from rich.progress import track
from rich.prompt import Prompt

input = Prompt.ask

# 1. Define a Hacker/Gamer Theme
custom_theme = Theme(
    {
        "neon_green": "bold #00ff00",
        "neon_magenta": "bold #ff00ff",
        "cyber_cyan": "bold #00ffff",
        "warning_yellow": "bold #ffff00",
        "dim_matrix": "dim #005500",
    }
)

# Initialize console with the custom theme
console = Console(theme=custom_theme)


def fetch_repository_intel(repo_name: str, branch_limit: int = 25) -> None:
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        console.print(
            "[red]/// ERROR: NO GITHUB_TOKEN DETECTED IN ENVIRONMENT ///[/red]"
        )
        return

    # Authenticate
    g = Github(auth=Auth.Token(token))

    try:
        # --- PHASE 1: FETCH GLOBAL STATS ---
        with console.status(
            f"[neon_green]Establishing secure uplink to {repo_name}...[/neon_green]",
            spinner="bouncingBar",
        ):
            repo = g.get_repo(repo_name)

            # Gather Vital Stats
            stars = repo.stargazers_count
            updated = repo.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            pushed = repo.pushed_at.strftime("%Y-%m-%d %H:%M:%S")
            size_mb = f"{repo.size / 1024:.2f} MB"

            # Gather Community & Structure (Takes slightly longer)
            contributors = repo.get_contributors().totalCount
            releases = repo.get_releases().totalCount
            deployments = repo.get_deployments().totalCount
            branches = list(repo.get_branches())
            total_branches = len(branches)

            # Safe fetch for License
            try:
                license_name = repo.get_license().license.name
            except GithubException:
                license_name = "UNKNOWN / ENCRYPTED"

            # Safe fetch for README
            try:
                readme = repo.get_readme()
                readme_size = f"{len(readme.decoded_content):,} bytes"
            except GithubException:
                readme_size = "NOT FOUND"

        # --- BUILD UI: GLOBAL STATS TABLE ---
        stats_table = Table(
            title=f"[neon_magenta]/// GLOBAL REPOSITORY INTEL : {repo.full_name.upper()} ///[/neon_magenta]",
            border_style="cyber_cyan",
            header_style="warning_yellow",
            expand=True,
            show_lines=True,
        )

        stats_table.add_column("DATABANK", justify="left", style="neon_green")
        stats_table.add_column("METRIC", justify="left", style="cyber_cyan")
        stats_table.add_column("VALUE", justify="right", style="warning_yellow")

        # Add Rows
        stats_table.add_row("VITAL STATS", "Stars (Reputation)", f"{stars:,}")
        stats_table.add_row("", "Last Updated", updated)
        stats_table.add_row("", "Last Pushed", pushed)
        stats_table.add_row("CODEBASE", "Total Branches", str(total_branches))
        stats_table.add_row("", "Repository Size", size_mb)
        stats_table.add_row("COMMUNITY", "Contributors", str(contributors))
        stats_table.add_row("", "Releases", str(releases))
        stats_table.add_row("", "Deployments", str(deployments))
        stats_table.add_row("METADATA", "License", license_name)
        stats_table.add_row("", "README Payload Size", readme_size)

        # Render Global Stats
        console.print("\n")
        console.print(Panel(stats_table, border_style="neon_green"))

        # --- PHASE 2: FETCH & BUILD BRANCH INTEL ---
        branches_to_process = branches[:branch_limit]

        branch_table = Table(
            title=f"[neon_magenta]/// ACTIVE BRANCH MATRIX (TOP {len(branches_to_process)}) ///[/neon_magenta]",
            border_style="neon_green",
            header_style="cyber_cyan",
            expand=True,
            show_lines=True,
        )

        branch_table.add_column(
            "BRANCH ID", justify="left", style="neon_green", no_wrap=True
        )
        branch_table.add_column(
            "LAST MODIFIED BY", justify="left", style="warning_yellow"
        )
        branch_table.add_column("TIMESTAMP (UTC)", justify="center", style="cyber_cyan")
        branch_table.add_column("LATEST SHA", justify="right", style="dim white")

        console.print(
            f"\n[cyber_cyan]Scanning top {len(branches_to_process)} of {total_branches} total branches...[/cyber_cyan]"
        )

        for branch in track(
            branches_to_process, description="[neon_green]Decrypting commit logs..."
        ):
            # Fetch specific commit object for author and date
            commit = repo.get_commit(branch.commit.sha)

            branch_name = branch.name
            author_name = commit.commit.author.name
            date_modified = commit.commit.author.date.strftime("%Y-%m-%d %H:%M:%S")
            short_sha = branch.commit.sha[:7]

            branch_table.add_row(
                f"> {branch_name}", author_name, date_modified, short_sha
            )

        # Render Branch Table
        console.print("\n")
        console.print(
            Panel(
                branch_table,
                border_style="neon_magenta",
                title="[cyber_cyan]DATA EXTRACTION COMPLETE[/cyber_cyan]",
                title_align="left",
            )
        )

    except GithubException as e:
        console.print(
            f"\n[bold red]/// CONNECTION TERMINATED: {e.data.get('message', 'Unknown Error')} ///[/bold red]"
        )


def extract_repo_id(input_string: str) -> str:
    clean_target = input_string.strip().rstrip("/")
    clean_target = re.sub(r"\.git$", "", clean_target)

    if "github.com/" in clean_target:
        clean_target = clean_target.split("github.com/")[1]

    parts = clean_target.split("/")

    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"

    return clean_target


def take_repo_input():
    data = ""
    try:
        with open("./cache/repo", "r") as file:
            data = file.read()
            repo = data
            # print(data)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass

    # Build the prompt dynamically
    if data:
        data_text = f" ([neon_magenta]P : Previous repo {data}[/neon_magenta])"
    else:
        data_text = ""

    prompt_text = f"[cyber_cyan]> TARGET DATABANK (user/repo) [red bold](Q : Quit)[/red bold]{data_text}\n> [/cyber_cyan]"

    user_choice = console.input(prompt_text)

    if user_choice.lower() == "q" or user_choice == "":
        exit()

    console.clear()

    if user_choice.lower() == "p" and data:
        return repo

    repo = extract_repo_id(user_choice)

    os.makedirs("./cache", exist_ok=True)

    try:
        with open("./cache/repo", "w") as file:
            file.write(repo)
    except FileNotFoundError:
        print("[red bold]ERROR: Failed to create cache directory/file.[/]")
    except PermissionError:
        print(
            "[red bold]ERROR: You do not have the required clearance to write cache file.[/]"
        )

    return repo


if __name__ == "__main__":
    # Change this to whatever repo you want to scan
    # TARGET_REPO = "raspberrypi/rpi-imager"
    TARGET_REPO = take_repo_input()

    # Run the uplink
    fetch_repository_intel(TARGET_REPO)
