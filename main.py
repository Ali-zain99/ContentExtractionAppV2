from flask import Flask, request, jsonify, render_template, send_from_directory # pyright: ignore[reportMissingImports]
from Header_Extractor import extract_header_links, clean_header_links
from Header_link_Extractor import extract_links_from_header_json
from Header_mindmaps import generate_mindmaps_from_headers
from Merge_All_Header_Mindmap import merge_mindmaps
from Validation_Mindmap import validation
from Screenshot_node import Screenshot_Node
# from Header_Extractor_After_Login import login_section
# from popup import login_section
from zip import zip_folder
import json
import asyncio
import os
import sys
import traceback

# CRITICAL: Use ProactorEventLoop for Windows + Playwright subprocess support
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    url = data.get('url')
    headless = data.get('headless', True)
    username = data.get("username","").strip()
    password = data.get("password","").strip()


    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        print(f"Extracting links from: {url}")
        from domain_extractor import extract_domain
        folder_name = extract_domain(url)
        print("Creating Folder with domain name")
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"folder created with {folder_name} name")
        else:
            print(f"!!!!!!!!!!!!!!!!!!! {folder_name} folder already created!!!!!!!!!!!!!")
        # Run the async function from sync context
        asyncio.run(extract_header_links(url, folder_name, headless=headless))
        
        # Clean the extracted links
        input_file = os.path.join(folder_name, "header_links.json")
        
        if not os.path.exists(input_file):
            return jsonify({'error': 'Failed to create header_links.json file'}), 500
        
        # Clean and get the links
        cleaned_links = clean_header_links(input_file, input_file)
        print(f"Successfully extracted and cleaned {len(cleaned_links)} links")
        try:
            print("🚀 Starting header link extraction process...")

            # --- Extract header links ---
            extract_links_from_header_json(header_json_path=input_file, base_folder=folder_name)
            print("✅ Header links extracted successfully.")

            # --- Determine domain folder from input file ---
            domain_folder = os.path.dirname(input_file)
            if not domain_folder:
                domain_folder = "."

            # --- Define headers folder path ---
            headers_folder = os.path.join(domain_folder, "headers")

            # --- Check if headers folder exists ---
            if os.path.isdir(headers_folder):
                print(f"📂 Found headers folder {headers_folder}. Starting MindMap generation...")

                # 🧠 Generate MindMaps for all header link files
                asyncio.run(generate_mindmaps_from_headers(base_folder=folder_name))
                print("✅ MindMaps created from header links.")

                # 🔗 Merge all generated MindMaps
                print("🔄 Merging all header MindMaps...")
                merge_mindmaps(base_folder=domain_folder)
                print("✅ Merged all header MindMaps successfully.")

                # ✅ Validate the final merged structure
                print("🧩 Starting validation...")
                validation(base_folder=folder_name)
                print("✅ Validation complete.")

                # 🖼️ Take screenshots of nodes
                print("📸 Capturing screenshots for MindMap nodes...")
                asyncio.run(Screenshot_Node(base_folder=folder_name))
                print("✅ Screenshots integrated into MindMap.")

                # 👤 Handle login-related processing if credentials provided
                if username and password:
                    print("🔐 Starting login section...")
                    from ScreenShot_node_After_Login import login_and_get_context
                    from playwright.async_api import async_playwright

                    async def main_login():
                        async with async_playwright() as p:
                            browser, context = await login_and_get_context(p, username, password, headless)
                            if context:
                                # Continue with the rest of the after-login process
                                from Header_Links_Ectractor_After_Login import extract_header_links_and_screenshots
                                from Header_mindmaps_after_login import header
                                from Merge_all_header_mindmap_After_Login import merge_mindmaps
                                from Validation_Mindmap_After_login import validation_after_login

                                await extract_header_links_and_screenshots(username, password, domain_folder, headless=headless)
                                await header(base_folder=domain_folder)
                                merge_mindmaps(base_folder=domain_folder)
                                validation_after_login(base_folder=domain_folder)
                            await browser.close()

                    asyncio.run(main_login())

                    print("📸 Capturing screenshots after login...")
                    from ScreenShot_node_After_Login import Screenshot
                    asyncio.run(Screenshot(username=username, password=password, base_folder=domain_folder))
                    print("✅ Screenshots after login captured.")

                    # 🧠 Merge all MindMaps into a single file
                    print("🔄 Merging all MindMaps into one unified file...")
                    from Merge import generating_full_mindmapp
                    generating_full_mindmapp(base_folder=domain_folder)
                    print("✅ Unified MindMap generated.")

                    # 📝 Add button descriptions
                    print("🧾 Adding button descriptions to final MindMap...")
                    from button_description import process_mindmap

                    INPUT_MM = os.path.join(domain_folder, "Merged_Website_Structure.mm")
                    OUTPUT_MM = os.path.join(domain_folder, "Full_Website_Structure_updated_with_descriptions.mm")

                    if not os.path.exists(INPUT_MM):
                        print(f"❌ {INPUT_MM} file not found.")
                    else:
                        process_mindmap(INPUT_MM, OUTPUT_MM)
                        print("✅ Button descriptions added successfully.")

                        # --- Zip the entire folder after final file creation ---
                        try:
                            output_zip_file = f"{folder_name}.zip"
                            zip_folder(folder_name, output_zip_file)
                            print(f"✅ Successfully zipped the folder to {output_zip_file}")
                        except Exception as e:
                            print(f"❌ Error during zipping: {e}")
                            return jsonify({
                                'error': f"Failed to zip the folder: {e}",
                                'details': traceback.format_exc()
                            }), 500

                else:
                    print("⚠️ No username/password provided — skipping login section.")
                    # --- Zip the folder if no login is provided ---
                    try:
                        output_zip_file = f"{folder_name}.zip"
                        zip_folder(folder_name, output_zip_file)
                        print(f"✅ Successfully zipped the folder to {output_zip_file}")
                    except Exception as e:
                        print(f"❌ Error during zipping: {e}")
                        return jsonify({
                            'error': f"Failed to zip the folder: {e}",
                            'details': traceback.format_exc()
                        }), 500

            else:
                print(f"❌ Headers folder not found at path: {headers_folder}")

        except Exception as e:
            error_msg = f"An error occurred during MindMap generation: {str(e)}"
            print(f"❌ {error_msg}")
            print(traceback.format_exc())
            return jsonify({
                'error': error_msg,
                'details': traceback.format_exc()
            }), 500

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        print(f"Error during extraction: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            'error': error_msg,
            'details': traceback.format_exc()
        }), 500

    # ✅ Return cleaned result to API response
    return jsonify({
        'success': True,
        'count': len(cleaned_links),
        'links': cleaned_links,
        'zip_file': f"{folder_name}.zip"
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=False)
    # try:
    #     print("start Extract_links_from_header_json file")
    #     extract_links_from_header_json(header_json_path="header_links.json")
    #     try:
    #         path = "header"
    #         if os.path.isdir(path):
    #             print("Starting MindMap generation")
    #             generate_mindmaps_from_headers()
    #             # asyncio.run(generate_mindmaps_from_headers())
    #             print('################## Mindmap is created using Header links ##########################')
    #         else:
    #             print(f"path isn't Available {path}")
    #     except Exception as e:
    #         error_msg_of_mindmapp_generation = str(e)
    #         print(f"error occurs in Mindmapp generation side :{error_msg_of_mindmapp_generation}")
    # except Exception as e:
    #     error_msg_of_header_link = str(e)
    #     print(f"error occurs in header link extractor side :{error_msg_of_header_link}")

    
