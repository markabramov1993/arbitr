# BoTTube mobile login reports success without validating the API key

## Summary

The official BoTTube mobile client can report a successful login for an invalid API key.

`mobile-app/src/api/client.ts::login(agentName, apiKey)` says it validates credentials, but it actually fetches the **public** agent profile endpoint with authentication explicitly disabled. If the named public agent exists, the client saves whatever API-key string the user supplied.

`mobile-app/src/hooks/useAuth.ts` then treats that returned public profile as a successful login and immediately sets `isAuthenticated = true`.

This does **not** bypass BoTTube server authorization. Instead, it creates a false-success authentication state in the official client: the user appears signed in until the first protected request rejects the invalid key (or the app is restarted and session initialization revalidates through `getMe()`).

## Current source

In `mobile-app/src/api/client.ts`:

```ts
async login(agentName: string, apiKey: string): Promise<Agent> {
  // Validate credentials by fetching profile
  const agent = await this.request<Agent>(`/api/agents/${agentName}`, {
    method: 'GET',
  }, false);

  if (agent) {
    await this.saveSession(apiKey, agentName);
  }

  return agent;
}
```

The final `false` is the `includeAuth` argument, so no `X-API-Key` is sent.

The repository API documentation explicitly defines this route as public:

```text
GET /api/agents/<agent_name>
Get a public agent profile and their videos. No auth required.
```

By contrast, the mobile client uses `getMe()` for an authenticated session check:

```ts
async getMe(): Promise<Agent> {
  return this.request<Agent>('/api/agents/me');
}
```

In `mobile-app/src/hooks/useAuth.ts`, the immediate login path is:

```ts
const profile = await api.login(agentName.trim().toLowerCase(), apiKey.trim());
setAgent(profile);
setIsAuthenticated(true);
```

The mount/restart path is stricter: it calls `api.getMe()` and clears an invalid session if that protected call fails. This difference is what makes the bug user-visible immediately after login.

## Deterministic reproduction

No production write or credential is required.

1. Pick the name of any existing public BoTTube agent.
2. In the mobile app login form, enter that agent name and any non-empty fake key, for example `definitely-not-a-real-key`.
3. `api.login()` requests only the public `/api/agents/<name>` endpoint, with `includeAuth=false`.
4. The public profile request succeeds because the agent exists.
5. `saveSession()` stores the fake key.
6. `useAuth.login()` receives the profile and sets `isAuthenticated=true`.
7. Call a protected method such as `getMe()`; the server rejects the fake key.

The invalid credential therefore passes the UI's login boundary and is persisted even though it was never validated.

## Expected behavior

The login operation should prove that the supplied API key belongs to a valid authenticated session before saving it or setting authenticated UI state.

A minimal fix is to stage the key in memory and validate it against an authenticated endpoint such as `/api/agents/me`; only after a successful response should the session be persisted. The returned authenticated profile can then be compared with the requested `agentName` if the UI continues to request both values.

Invalid keys should reject the login promise and leave `isAuthenticated=false` with no stored session.

## Actual behavior

Any key string is accepted and persisted when paired with the name of an existing public agent. The UI reports authenticated success until a later protected call exposes the invalid credential.

## Impact

- false-positive login state in the official mobile client;
- invalid credentials are written into secure storage;
- the user can enter authenticated UI flows only to receive 401s later;
- error attribution becomes misleading because credential failure appears on an unrelated later action rather than at login;
- behavior differs between immediate login and app restart/session hydration.

There is no claim of server-side authentication bypass: protected endpoints still enforce the key.

## Duplicate check

Searched current open and closed `Scottcjn/bottube` issues for combinations of:

- mobile login invalid API key;
- `saveSession` + `apiKey`;
- public profile + login;
- mobile authentication / credential validation.

No issue was found describing this exact false-success mobile login path. Recent SDK auth issue #2236 is different: it concerns the TypeScript SDK dropping a configured API key from protected requests. This finding concerns `mobile-app/src/api/client.ts::login()` never validating the supplied key in the first place.

## Source references

- `mobile-app/src/api/client.ts` — `login()`, `saveSession()`, `getMe()`
- `mobile-app/src/hooks/useAuth.ts` — successful login state transition and restart revalidation
- `docs/API.md` — `/api/agents/<agent_name>` is explicitly public/no-auth

## Bounty accounting

Submitted as the **second and final item** for `markabramov1993` under `Scottcjn/rustchain-bounties#1102` (`cap: 2`). Requested classification: functional bug, **5 RTC**, subject to maintainer verification.

RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`

AI assistance disclosure: source inspection, duplicate checking, and report preparation were performed with OpenAI assistance under operator authorization. No production state-changing request, credential guessing, or authentication bypass attempt was performed.
