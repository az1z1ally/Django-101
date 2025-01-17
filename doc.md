## DJANGO STATIC FILES

`In Django, CSS, JavaScript, images, and other external files are referred to as static files. This terminology is used because these files are static, meaning they do not change in response to user inputs or interactions. They remain the same and are served directly to the user's browser without any server-side processing.`

## Key Points:

1. ### Unchanging Content:

- Static files contain fixed content that doesn't change unless manually updated by the developer.

- Examples include stylesheets (CSS), scripts (JavaScript), images, fonts, and other assets that enhance the presentation and functionality of a web application.

2. ### Client-Side Execution:

- These files are sent to the client's browser where they are executed or rendered.

- CSS defines the look and feel of the application, JavaScript provides interactive functionalities, and images and fonts contribute to the visual elements.

3. ### Efficiency:

- Serving static files is efficient because they can be cached by the browser, reducing load times and server requests on subsequent visits.

- Since they are not generated dynamically, they can be delivered quickly to enhance user experience.

4. Django's Handling:

- Django provides tools and configurations to manage and serve static files efficiently.

- The `STATIC_URL, STATICFILES_DIRS and STATIC_ROOT` settings in settings.py help in defining how and where static files are stored and served.

- During development, the `django.contrib.staticfiles `app makes it easy to serve static files locally. In production, these files are typically served by a web server or CDN (Content Delivery Network).

`In settings.py`

#### URL to use when referring to static files

`STATIC_URL = 'static/'`

#### URL to use when referring to user uploaded contents

`MEDIA_URL = '/uploads/'`

#### Directories where Django will look for static files

`STATICFILES_DIRS = [
  BASE_DIR / 'static',
]
`

#### Directory where user uploaded contents will be stored

`MEDIA_ROOT = BASE_DIR / 'static/uploads'`

#### Directory where collected static files will be stored

`STATIC_ROOT = BASE_DIR / 'staticfiles'`

## NEXT PARAMETER

In Django, the next parameter is typically used for redirection purposes. It's a common pattern in authentication flows, especially when you want to redirect users to a specific page after they log in. The next parameter in the URL contains the path to the destination page the user initially attempted to visit before being prompted to log in.

For example, if a user tries to access a restricted page, like `/dashboard`, but isn't logged in, they might be redirected to the login page with a URL like this: `/login/?next=/dashboard`. After successful authentication, your login view can use the next parameter to redirect the user back to `/dashboard`.

#### Here's a brief breakdown:

1. `User Attempts to Access a Restricted Page:` A user tries to go to a page that requires authentication.

2. `Redirection to Login Page with next Parameter:` They are redirected to the login page with the next parameter in the query string, indicating where they wanted to go.

3. `After Login:` Upon successful login, the view retrieves the next parameter value and redirects the user to that page.

Using the next parameter ensures a smooth user experience by taking them directly to the page they intended to visit, rather than a default page.
