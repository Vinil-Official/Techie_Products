# LeadFlow

LeadFlow keeps generated leads in browser LocalStorage and sends them to the existing FastAPI analysis endpoint. Saving a lead to Supabase is a separate, explicit action; Supabase records are private to the signed-in account and do not replace or modify the generated-lead list.

## Frontend Setup

```powershell
npm install
Copy-Item .env.example .env.local
npm run dev
```

Set these values in `.env.local`, then restart Vite:

```dotenv
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-publishable-or-anon-key
```

These are the Supabase project URL and browser-safe publishable/anon key. Never put a service-role key in a `VITE_` variable or frontend file. `.env.local` is ignored by Git.

## Supabase Setup

1. Create a Supabase project and enable the Email provider under Authentication settings.
2. In the SQL Editor, run [`supabase/qualified_leads.sql`](supabase/qualified_leads.sql). It creates the `qualified_leads` table, status and score constraints, source-lead uniqueness, and owner-scoped RLS policies.
3. Put the project URL and publishable/anon key from Supabase API settings in the frontend `.env.local` as `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.
4. Add the same values to the existing backend `.env` as `SUPABASE_URL` and `SUPABASE_ANON_KEY`. The backend uses the anon key together with the user's bearer token, so Supabase RLS still enforces row ownership. Do not use a service-role key.
5. Configure the site URL and allowed redirect URLs in Supabase Authentication settings for the local frontend and deployed frontend. Email confirmation may remain enabled; a new user must confirm their email before signing in if it is required by the project.
6. Create an account or sign in from the Qualified Leads section. RLS only permits authenticated owners to access their own rows; no public write policy or service-role credential is used.

## Backend Setup

The FastAPI/LangGraph backend lives in `../../backend`. Add `SUPABASE_URL` and `SUPABASE_ANON_KEY` to its existing `.env` (keep the existing `GROQ_API_KEY` there). From that backend directory, activate its virtual environment and install requirements if needed, then start the API:

```powershell
..\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The Vite proxy forwards `/qualified-leads` to FastAPI during development. For deployment, set `VITE_API_BASE_URL` in the frontend and `FRONTEND_ORIGINS` in the backend environment.

## Lead Workflow

Generated results are still stored under the `ai_lead_generation_leads` LocalStorage key. Choose **Add to Database** for a generated result, review or edit its values, choose a qualification or pipeline status, and confirm. The browser sends the operation to FastAPI with the current Supabase session token; FastAPI forwards that token and the anon key to Supabase, where RLS authorizes the owner. A unique `(owner_id, source_lead_id)` index prevents duplicate saves for the same generated lead. Failed requests leave the LocalStorage record untouched. The Qualified Leads view loads actual Supabase records and supports search, status filtering, pagination, viewing, editing, and confirmed deletion.

## Verification

1. Start the FastAPI backend and frontend, then process a lead. Confirm it appears in Processed Leads and remains after refreshing the browser.
2. Sign in, choose **Add to Database**, change the status or notes, and save. Confirm the success message appears after the request completes and the action changes to **Already Added**.
3. Open **Qualified Leads** and confirm the record, status, score, and created date are present. Refresh the view and confirm it is still present.
4. Use **View** to inspect details; use **Edit** to change the status or score and confirm the table refreshes.
5. Use **Delete**, cancel once to verify the record remains, then confirm deletion and refresh to verify it is gone.
6. Try a blank business name, malformed phone/website, or score outside 0–100; inline errors should block submission. Sign out and verify database rows are no longer displayed.

Run `npm run lint` and `npm run build` for frontend checks. FastAPI exposes interactive route documentation at `http://127.0.0.1:8000/docs`. A live Supabase project is required to verify actual database CRUD end to end.