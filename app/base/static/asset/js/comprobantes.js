$(document).ready(function() {

    if (!$.fn.DataTable.isDataTable('#tabla_comprobantes')) {

        // Buscar índice de la columna Vencimiento
        var indiceFecha = $('#tabla_comprobantes thead th')
            .filter(function() {
                return $(this).text().trim().toLowerCase() === "vencimiento";
            })
            .index();

        $('#tabla_comprobantes').DataTable({
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100],

            // 🔥 AQUÍ SE APLICA EL TIPO DE FECHA
            columnDefs: [
                {
                    type: 'date-eu',
                    targets: indiceFecha
                }
            ],

            order: [[indiceFecha, 'desc']],
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
