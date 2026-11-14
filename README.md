\# Pet Care Finder



A web app where pet owners find and book trusted vets, groomers, pet sitters and trainers near them.

Built by \*\*\[Sumiya Shimu Akhy-22701070]\*\* for \*\*\[Mobile Apps Development]\*\*.



\## Features



| # | Required feature | What was built | Status |

|---|---|---|---|

| 1 | ERD | `docs/petcare\_erd.pdf` (8 tables) | Done |

| 2 | Real-time commenting | Reviews and comments on provider pages, refreshed every 5 seconds without reloading | Done (polling) |

| 3 | Like / dislike with live count | Reactions on provider pages | Done (polling) |

| 4 | Real-time unique username check | Checks the database while typing on sign up | Done |

| 5 | Email and phone verification | Email OTP by Gmail SMTP. Phone OTP with rate limits and a daily cap | Email done. Phone works in demo mode (code printed in terminal); no SMS gateway connected yet |

| 6 | Multiple text boxes and dropdown lists | Provider profile, search, booking and pet forms | Done |

| 7 | Interactive rating system | 1 to 5 stars with live average | Done |

| 8 | Pagination | Provider list (server side) and browse page (Vue) | Done |

| 9 | Embedded video | YouTube demo video on provider pages | Done |

| 10 | Maps | Embedded Google map, "Near me" sorting using the browser GPS | Done (map iframe, not the Maps JavaScript API) |

| 11 | Sessions | Django session login and logout | Done (session based, no JWT) |

| 12 | On-device ML | TensorFlow.js (MobileNet) detects dog, cat, bird or rabbit from a photo inside the browser. Also server side Smart Match with scikit-learn | Done |

| 13 | Image upload with cloud storage | Provider photos stored on Cloudinary | Done |

| 14 | Datepicker | Booking date picker | Done |

| 15 | Animations | GSAP page animations | Done |

| 16 | SASS or Tailwind | Tailwind CSS (CDN) | Done |

| 17 | Git, collaboration tools | Git and GitHub, GitHub Actions | Done |

| 18 | GraphQL | `/graphql/` (graphene-django) | Done |

| 19 | REST API | `/providers/api/` (Django REST Framework) | Done |

| 20 | Crystal Report | | Not done |

| 21 | Modern frontend framework | `/providers/browse/` is built with Vue 3 (loaded from a CDN, no build step) | Partly done |

| 22 | Containerization / CI | `Dockerfile` and GitHub Actions workflow (checks, tests, Docker build) | Done |

| 23 | Generative AI | AI assistant (Gemini API) that recommends providers | Done |

| 24 | TBD | | Waiting for the announcement |



\## Tech stack



Python, Django, Django REST Framework, graphene-django, SQLite, scikit-learn, TensorFlow.js, Vue 3, Tailwind CSS, GSAP, Cloudinary, Gemini API, Docker, GitHub Actions.



\## Run it locally



&#x20;   python -m venv venv

&#x20;   venv\\Scripts\\activate

&#x20;   pip install -r requirements.txt

&#x20;   python manage.py migrate

&#x20;   python manage.py createsuperuser

&#x20;   python manage.py runserver



Open http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin/.

A provider appears in the public list only after an admin ticks \*\*Is verified\*\*.



\## Secret files (never committed)



These files are listed in `.gitignore`. Each one is optional and the site still runs without it:



| File | What it is for |

|---|---|

| `email\_password.txt` | Gmail app password for sending email codes |

| `ai\_key.txt` | Gemini API key for the AI assistant |

| `cloudinary.txt` | Two lines: Cloudinary cloud name, then the unsigned upload preset |



Without `cloudinary.txt` photos are saved on the local disk. Without `ai\_key.txt` the AI assistant shows a "not set up" message. Without `email\_password.txt` sign up cannot send the email code.



\## Notes



\- Phone verification runs in demo mode (`SMS\_MODE = 'console'` in `config/settings.py`). Real SMS needs a paid SMS gateway.

\- The AI assistant and the pet photo detector can make mistakes.

