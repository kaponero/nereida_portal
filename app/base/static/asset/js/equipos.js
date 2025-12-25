$(document).ready(function () {

    if (!$.fn.DataTable.isDataTable('#tabla_equipos')) {

        $('#tabla_equipos').DataTable({
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100],

            // 🔥 Ordenar por la columna "Nombre"
            order: [[0, 'asc']], // ascendente A → Z

            stripeClasses: ['even', 'odd'],
            language: {
                decimal: "",
                emptyTable: "No hay datos disponibles",
                info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
                infoEmpty: "Mostrando 0 a 0 de 0 registros",
                infoFiltered: "(filtrado de _MAX_ registros totales)",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ registros",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                search: "Buscar:",
                zeroRecords: "No se encontraron resultados",
                paginate: {
                    first: "Primero",
                    last: "Último",
                    next: "Siguiente",
                    previous: "Anterior"
                }
            }
        });
    }
});
