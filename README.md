# Rocketdreams System- Software Engineer Interview Task (2026) - Slava Kagan

## -- DEMO --
[![Watch Demo](https://img.shields.io/badge/Watch-Demo%20Video-blue)]https://bit.ly/Odysight-demo <br />
<br /> ![Demo](Screenshots/dashboard-demo.png)

## -- Overview --
The Meridian Casino & Resort is a luxury destination in Las Vegas. <br />
This system is a voice-based AI concierge system for the resort that allows guests to ask questions and receive instant, spoken answers about property, amenities, and services. <br />
The system should capture questions can't answer so the team can continuously improve coverage.

## -- Goals --
Core Goals
1. Provide 24/7 instant voice support for common guest questions.
2. Capture unanswered questions for later review.
3. Maintain the luxury, personalized feel guests expect from The Meridian.
4. Provide a playground interface to test the voice concierge.

## -- How to use this service || Prerequisites --
1. Docker Desktop, Install- https://www.docker.com/products/docker-desktop/ <br />
   Run it on background.
2. GIT Install- https://git-scm.com/
3. Open Terminal from any Operation System.
4. git clone ```https://github.com/SlavaKagan/Rocketdreams-Voice-Concierge-SK-Task-2026.git```
   cd Rocketdreams-Voice-Concierge-SK-Task-2026
5. Create a root .env file with your own API keys:
   OPENAI_API_KEY=...
   LIVEKIT_URL=wss://...
   LIVEKIT_API_KEY=...
   LIVEKIT_API_SECRET=...
   ELEVENLABS_API_KEY=...
   ELEVEN_API_KEY=...
   DEEPGRAM_API_KEY=...
6. From the project root, run:
```docker compose up --build```
7. Access the Site-
Open a browser and go to: ```http://localhost:3000```
The client app should be running and connected to the container.
8. At the end of use, stop the site- ```docker-compose down``` or just shutdown the terminal.

## -- System Architecture --
**Cameras → Processing Unit (PU) → App** <br /> <br />
![System Architecture Diagram](Screenshots/System%20Architecture.png)

## -- Tech Stack --
**GitHub repository:** ```https://github.com/SlavaKagan/Rocketdreams-Voice-Concierge-SK-Task-2026``` <br />

**Backend (mock backend server):**  <br />
The goal is to simulate a realistic PU API quickly. <br />
Provides all required API endpoints for the features described below. <br />
**```Python + FastAPI```**- very clean API definitions, async-native, auto-generates OpenAPI docs with swagger built in. <br />

**Admin-Frontend:**  <br />
```Vite dev server in Docker``` <br />
**```React + Vite```** is data-rich, fast to develop, lightweight, and the right tool for a real-time dashboard. <br />
React's component model is a natural fit for a UI with many independent, updating pieces- live camera feeds, status badges, result tables, and alert streams all update independently. <br />
**```Typescript```** <br/>
TypeScript is a superset of JavaScript that adds static types. It compiles away at build time- the browser still runs plain JavaScript. The benefit is entirely during development. <br /> Without TypeScript, every renamed type, the frontend would silently break-undefined in the UI. <br />
TypeScript turns runtime bugs into compile-time errors <br />
**```Tailwind CSS v4```** <br/>
Utility-first CSS with zero runtime overhead. Chosen for rapid development of a consistent, dark industrial UI without introducing a heavy component library. <br/>

**Combination of the stack:**  <br />
**```Docker Compose```**- one command <br />
Operational maturity. A system like this would run on an edge device (the PU itself), so containerization is a natural fit. Single-command startup also respects the reviewer's time. ``` "docker compose up" ``` <br />

```Frontend → http://localhost:3000 ``` <br />
```Backend API → http://localhost:8000 ```<br />
```API Docs (Swagger) → http://localhost:8000/docs ``` <br />

## -- System Features--

## -- Architecture rationale --
*REST API endpoints- HTTP Methods <br />

**Cameras** <br/>
| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | GET | /cameras | List all cameras 
| 2 | GET | /cameras/{id} | Get single camera details
| 3 | PATCH | /cameras/{id}/settings | Update camera parameters (gain, exposure, rotation)
| 4 | GET | /cameras/{id}/stream | WebSocket- live stream frames

## -- Tests Section --
```Vitest```- Test runner. <br>
```React Testing Library (RTL)```- renders components in a simulated DOM. <br>
```UserEvent```- simulates user clicks and typing. <br>

## -- Optimize the system+Future tasks --
** In order to make the system better and to improve it I thought on few things that I would done for later in production:
1. Test Reference and Automation- Frontend + Backend
   * Unit Test
   * Integration Tests
2. Add important logs through the system + Performance.
3. Security- Authentication and Authorization.
4. Rate Limiting.
5. Terraform to deploy to AWS.
6. Upload the system to server like Render- A free one

## -- Contact --
**Full Name:** Slava Kagan <br>
**Email:** <slava.kagan.ht@gmail.com> <br>
**Phone Number:** 055-3187648 <br>

## -- License --
```Rocketdreams Company Task```