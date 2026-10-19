1.first activate virtual enviroment by (in bash)
Mobile Programming@DESKTOP-1RP2FAM MINGW64 /c/local-rag-project/backend (main)
$ source .venv/Scripts/activate
(.venv)
Mobile Programming@DESKTOP-1RP2FAM MINGW64 /c/local-rag-project/backend (main)

---

2.checking running container status also in this project postgre sql i am using local one so also start pgadmin as well in local and check docker running containers like this.
Mobile Programming@DESKTOP-1RP2FAM MINGW64 /c/local-rag-project/backend (main)
$ docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
b80eeb53d0b1 localstack/localstack:4.10.0 "docker-entrypoint.sh" 7 days ago Up 5 minutes (healthy) 0.0.0.0:4566->4566/tcp, [::]:4566->4566/tcp local-rag-localstack
71e234b591bb ollama/ollama:latest "/bin/ollama serve" 7 days ago Up 4 minutes 0.0.0.0:11434->11434/tcp, [::]:11434->11434/tcp local-rag-ollama
2d7c672d97a3 qdrant/qdrant:latest "./entrypoint.sh" 7 days ago Up 4 minutes 0.0.0.0:6333-6334->6333-6334/tcp, [::]:6333-6334->6333-6334/tcp local-rag-qdrant

---

3.Then run backend like this
Mobile Programming@DESKTOP-1RP2FAM MINGW64 /c/local-rag-project/backend (main)
$ python -m uvicorn app.main:app --reload --port 8000

---

4.Then run frontend as well

Mobile Programming@DESKTOP-1RP2FAM MINGW64 /c/local-rag-project/frontend (main)
$ ng s -o
Initial chunk files | Names | Raw size
polyfills.js | polyfills | 90.20 kB |
main.js | main | 8.69 kB |
styles.css | styles | 95 bytes |

                    | Initial total | 98.98 kB

Application bundle generation complete. [2.896 seconds]

Watch mode enabled. Watching for file changes...
NOTE: Raw file sizes do not reflect development server per-request transformations.
➜ Local: http://localhost:4200/
➜ press h + enter to show help

---

running evn
5.http://localhost:4200/ -frontend
6.http://localhost:8000/docs -backend
7.http://localhost:4566/documents -localstack s3 details
8.http://localhost:6333/dashboard#/collections -Qudrant document collection
9.http://localhost:11434/api/tags-ollama api tags

---

10. if you want to ask your queries in local by docker container running for ollama you can run this command and start asking your questions

Mobile Programming@DESKTOP-1RP2FAM MINGW64 /c/local-rag-project (main)
$ docker exec -it local-rag-ollama ollama run qwen2.5:3b

> > > what is js
> > > JavaScript, often abbreviated as JS, is a lightweight, interpreted or just-in-time compiled programming language commonly used
> > > for web development. It is one of the core technologies of the World Wide Web, used by most websites today to
> > > interactive elements (^[[10;117Rforms, widgets, and games) in a browser.

Here are some key points about JavaScript:

1. **Frontend Language**: It is primarily used to enhance the functionality and interactivity of websites. It can be embedded
   into HTML files to create dynamic web pages.

2. **Cross-Platform**: JavaScript is available in different versions (e.g., Node.js, a server-side JavaScript environment) and
   can be run on various platforms, including Windows, Mac, and Linux.

3. **Client-Side vs. Server-Side**: While the most common use of JavaScript is client-side (running in a user's browser), it
   can also be used server-side (for example, with Node.js) to create applications that run on the server side.

4. **Frameworks and Libraries**: JavaScript has a vast ecosystem of frameworks and libraries, such as React, Angular, Vue.js,
   and jQuery, which help developers build complex applications more efficiently.

5. **Versioning**: There are ongoing efforts to update the JavaScript specification (ECMAScript), and these updates are known
   as ECMAScript Editions. Each new edition (e.g., ECMAScript 2015) introduces new features and improvements.

6. **Interpreted**: JavaScript is typically interpreted by the web browser, although its syntax is similar to that of compiled
   languages. This means that the code is executed line-by-line, which can affect performance, especially for large or complex
   applications.

7. **Versatile**: JavaScript can be used to create applications that can run on the web, desktop (using Electron framework),
   and mobile platforms (with frameworks like React Native).

JavaScript is essential for anyone looking to develop web applications, and its versatility and widespread adoption make it a
valuable skill in the tech industry.

> > > what is angular updated version currently available
> > > As of my last update in October 2023, the current major version of Angular is Angular 15. Angular is a popular framework for
> > > building web applications, and new major versions are released periodically to add new features, improve performance, and
> > > address security concerns.

Here are the major versions of Angular that have been released and are currently available:

1. **Angular 15** (released in December 2023)
2. **Angular 14** (released in March 2023)

---
