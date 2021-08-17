<h1>Crawler- Instructions for deployement and use</h1><br>
<p>
    <span> <h2>Endpoints and description</h2><b></span>
    <table>
    <ul>
        <li>/api/register --> POST call to register a new user</li>
        <li>/api/signin -->  POST call to recieve authentication token for user</li>
        <li>/api/userdetails --> GET call to fetch user details according to passsed token in header</li>
        <li>/api/pdfcrawl --> GET call to crawl and parse a pdf on a fixed link</li>
        <li>/api/pdfcrawl/&#60;crawlLevel&#62; --> GET call to crawl and parse a pdf on a fixed link upto specified  levels</li>
        <li>/api/webcrawl --> GET call to crawl and parse after submitting a webpage on a fixed link</li>
    </ul>
    </table>
    <span>
    </br>The app can be tested on the following host: </br>
    <a href= http://15.206.122.190:8000/ >http://13.235.244.233:8000/</a>
    </span>
    <span>
    </br>The postman collection link also mentioned below for all sample requests to above mentioned endpoints and can be imported: </br>
    <a href= https://www.getpostman.com/collections/935fd7ac4dcfad8fe131 >https://www.getpostman.com/collections/935fd7ac4dcfad8fe131</a>
    </span>

</p></br>
<p>
    <span> <h2>Environment Variables to be set while deployment</h2><b></span>
    <h5>CRAWL_DB_NAME=postgres_database_name</br>
    CRAWL_DB_USERNAME=postgres_db_username</br>
    CRAWL_DB_PASSWORD=postgres_db_password</br>
    CRAWL_DB_HOST=postgres_db_host</br>
    CRAWL_DB_PORT=postgres_db_port</br>
    CRAWL_SECTER_KEY=django_secret_key</br><h5>
</p></br>


<p>
    <span> <h2>Deployement using Docker</h2><b></span>
    <p>
    <span> <h3>Pull from DockerHub</h3><b></span>
    <p>The built image is pushed to docker hub and can be pulled using --> </br><h4> docker pull arunavnarayan03/crawler-complete</h4></p>
    </p>
    <span> <h3>Build localy</h3><b></span>
    <p>The repository has a Dockerfile and one can localy build the image</p></br>
    </p>
</p></br>



