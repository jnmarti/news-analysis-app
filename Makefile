run-app:
	poetry run streamlit run ./news_analysis/app.py --server.enableCORS false --server.enableXsrfProtection false