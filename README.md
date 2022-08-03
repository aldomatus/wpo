# wpo-back

<h2>GET STARTED:</h2>
<ol>
  <li>Create migrations: <br>
  Be sure not to have old migrations in the folders of your apps
  <code>python manage.py makemigrations</code>
  </li>
  <li>run migrations: <br>
  <code>python manage.py migrate</code>
  </li>
  <li>Add to database: <br>
    <spam style="color:red">1. Se abre la consola de django:</spam> <br>
    <code>python manage.py shell</code> <br>
    <spam>2. Se importan los modelos de los paises y estados:</spam> <br>
    <code>from users.models import CtCountry, CtState, CtLocation</code> <br>
    <spam>3. Se instancian pais y estado para posteriormente guardarlos en la base de datos</spam><br>
    <code>pais = CtCountry(country_name = 'Sin País',
      country_slug = 'sin-pais', country_abbreviation = 'SP', country_political_division = 'NA', country_status = False)             </code><br>
    <code>pais.save()</code> <br>
    <code>estado = CtState(state_name = 'Sin Estado', state_slug =  'sin-estado', state_status = True, country_id = 1)</code> <br>
    <code>estado.save()</code> <br>
    <code>localidad = CtLocation(location_id = 1, location_name = 'sin-localidad', state_id = estado.state_id, location_slug = "http://www.com", location_status = 1)</code> <br>
    <code>localidad.save()</code> <br>
    <code>exit()</code>
  </li>
  <li>Create superuser: <br>
    <code>python manage.py createsuperuser</code></li>
</ol>
