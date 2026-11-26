# 360 SEO Expert

Browser-based SEO workspace MVP.

## Deploy on Render
This repository includes a Render Blueprint (render.yaml). In Render choose New → Blueprint, connect this repository, review the plan, and apply it. The service is configured for the free web-service plan; free instances may sleep when idle.

## Included tools
- On-page HTML audit (paste page HTML or source)
- Title and meta description checks
- Heading and image-alt checks
- Keyword frequency analysis
- SEO content brief generator
- Health endpoint at /health

## Run locally
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000

This is an MVP, not a replacement for Google Search Console, GA4, PageSpeed Insights or paid keyword databases. Those integrations require credentials and separate setup.
