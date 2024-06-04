from autolinkedin.linkedin import LinkedIn
import os
from dotenv import load_dotenv
load_dotenv()

settings = {
   
    "LINKEDIN_BROWSER": "Chrome",
    "LINKEDIN_BROWSER_HEADLESS": 0,
    "LINKEDIN_PREFERRED_USER": "data/user_not_preferred.txt",
    "LINKEDIN_NOT_PREFERRED_USER": "data/user_preferred.txt",
}

with LinkedIn(
    username=os.environ.get('email'),
    password=os.environ.get('password'),
    browser=settings.get("LINKEDIN_BROWSER"),
    headless=bool(settings.get("LINKEDIN_BROWSER_HEADLESS")),
) as ln:
    ln.login()
   
    # ln.remove_recommendations(min_mutual=0, max_mutual=50)

    # max_invitations = ln.WEEKLY_MAX_INVITATION - ln.count_invitations_sent_last_week()

    # print(max_invitations)

    # ln.withdraw_sent_invitations(max_remove=10, older_than_days=0)

    ln.send_invitations(
        max_invitations=3,
        min_mutual=0,
        max_mutual=1000,
        preferred_users=["data analyst"], 
        not_preferred_users=["Sportsman", "Doctor"],
        view_profile=True,
    )

    # ln.accept_invitations()