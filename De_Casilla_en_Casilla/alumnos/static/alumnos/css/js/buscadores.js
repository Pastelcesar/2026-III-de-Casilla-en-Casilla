function filtrarEquipos() {
    let input = document.getElementById('buscadorEquipos');
    let filtro = input.value.toLowerCase();
    let tabla = document.getElementById('tablaEquiposBody');
    let filas = tabla.getElementsByTagName('tr');

    for (let i = 0; i < filas.length; i++) {
      let textoFila = filas[i].textContent || filas[i].innerText;
      if (textoFila.toLowerCase().indexOf(filtro) > -1) {
        filas[i].style.display = "";
      } else {
        filas[i].style.display = "none";
      }
    }
}
function filtrarAlumnos() {
    let input = document.getElementById('buscadorAlumnos');
    let filtro = input.value.toLowerCase();
    let tabla = document.getElementById('tablaAlumnosBody');
    let filas = tabla.getElementsByTagName('tr');

    for (let i = 0; i < filas.length; i++) {
      let textoFila = filas[i].textContent || filas[i].innerText;
      if (textoFila.toLowerCase().indexOf(filtro) > -1) {
        filas[i].style.display = "";
      } else {
        filas[i].style.display = "none";
      }
    }
}