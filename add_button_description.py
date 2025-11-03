import os
import xml.etree.ElementTree as ET

# ========================
# Common button descriptions
# ========================
BUTTON_DESCRIPTIONS = {
    "home": "Navigates to the main landing page or dashboard.",
    "about": "Displays information about the organization or product.",
    "contact": "Opens contact form or company contact details.",
    "help": "Leads to FAQs, support tickets, or live chat.",
    "dashboard": "Centralized area showing user stats and quick actions.",
    "profile": "User profile details and account settings.",
    "logout": "Ends user session and logs out of the system.",
    "settings": "Allows customization of account, preferences, or system options.",
    "notifications": "Shows recent alerts or updates.",
    "language": "Lets users change website language or location preferences.",
    "login": "Opens authentication form to access user account.",
    "sign in": "Opens authentication form to access user account.",
    "register": "Allows new users to create an account.",
    "sign up": "Allows new users to create an account.",
    "forgot password": "Redirects to password recovery flow.",
    "reset password": "Lets user reset credentials via email or code.",
    "verify email": "Confirms user’s email after signup.",
    "continue as guest": "Lets user browse without logging in.",
    "submit": "Sends form data to the server.",
    "save": "Stores entered information without submitting.",
    "cancel": "Discards current input or closes the form.",
    "next": "Moves to the next step in a process or wizard.",
    "back": "Returns to the previous screen or step.",
    "upload": "Allows file or image upload.",
    "download": "Triggers file or report download.",
    "edit": "Opens item for modification.",
    "delete": "Permanently deletes selected record.",
    "add": "Creates a new entry or record.",
    "add new": "Creates a new entry or record.",
    "add member": "Adds a new team member.",
    "add to cart": "Adds selected product to shopping cart.",
    "checkout": "Proceeds to payment and order confirmation.",
    "subscribe": "Starts a subscription or membership plan.",
    "renew membership": "Extends current membership period.",
    "view order history": "Displays list of past purchases.",
    "manage users": "Opens user list and permission controls.",
    "view reports": "Displays analytics or performance reports.",
    "approve": "Accepts pending requests.",
    "reject": "Denies pending requests.",
    "export data": "Downloads dataset in Excel/CSV/PDF format.",
    "import data": "Uploads bulk records from file.",
    "generate report": "Creates a summarized document based on filters.",
    "assign role": "Updates user access levels.",
    "message": "Opens a direct message or chat box.",
    "comment": "Adds a note or feedback to an item.",
    "reply": "Responds to an existing comment or thread.",
    "share": "Shares content via link or social media.",
    "invite": "Sends an invitation to new team members.",
    "search": "Executes a search query across site data.",
    "filter": "Narrows down data using specific criteria.",
    "refresh": "Reloads the current page or data.",
    "view details": "Opens detailed information of selected item.",
    "print": "Sends current page or data to printer.",
    "expand": "Expands the section for more details.",
    "collapse": "Collapses the section to hide details.",
}

# ========================
# Helper Functions
# ========================
def normalize_text(text):
    """Normalize button text for comparison."""
    return text.lower().strip().replace("_", " ").replace("-", " ")

def add_description_nodes(input_file, output_file, verbose=False):
    """Reads a .mm file, adds description child nodes where applicable, and saves new file."""
    print(f"🔍 Reading: {input_file}")
    tree = ET.parse(input_file)
    root = tree.getroot()

    updated_count = 0

    for node in root.iter("node"):
        text = node.attrib.get("TEXT", "")
        normalized = normalize_text(text)

        # Match button description
        for key, desc in BUTTON_DESCRIPTIONS.items():
            if key in normalized:
                # Check if description already exists
                already_has = any(desc in (child.attrib.get("TEXT", "") or "") for child in node.findall("node"))
                if not already_has:
                    desc_node = ET.Element("node", TEXT=desc)
                    node.append(desc_node)
                    updated_count += 1
                    print(f"✅ Added description for: {text}")
                break

    # Save updated mindmap
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"\n💾 Saved updated mindmap: {output_file}")
    print(f"🧠 Total buttons updated: {updated_count}")

# ========================
# Main Runner
# ========================
if __name__ == "__main__":
    INPUT_MM = r"Merged_Website_Structure.mm"
    OUTPUT_MM = r"Full_Website_Structure_updated_with_descriptions.mm"

    if not os.path.exists(INPUT_MM):
        print("❌ Input file not found.")
    else:
        add_description_nodes(INPUT_MM, OUTPUT_MM)
