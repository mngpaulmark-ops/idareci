import shutil
import os

source_dir = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org"
output_filename = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi_yedek_15.09.2026"

print(f"Creating zip backup from {source_dir}...")
shutil.make_archive(output_filename, 'zip', source_dir)
print(f"Successfully created: {output_filename}.zip")
