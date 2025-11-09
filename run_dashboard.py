import sys
import os

# Add healthai_nexus to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'healthai_nexus'))

# Run streamlit
os.system('python -m streamlit run healthai_nexus/app_dashboard.py')
