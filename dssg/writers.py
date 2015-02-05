# """
# Tools to write to output directory.
# """

# import os

# from django.conf import settings

# def build_output_tree(source_dir):
#     os.mkdir(OUTPUT_DIR)
#     if os.path.isdir(os.path.join(source_dir, settings.STATIC_DIR)):
#         shutil.copytree(os.path.join(source_dir, settings.STATIC_DIR),
#                         os.path.join(settings.OUTPUT_DIR, settings.STATIC_DIR))
#     for
