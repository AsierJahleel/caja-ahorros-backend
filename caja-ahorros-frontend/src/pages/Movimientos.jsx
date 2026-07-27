import { useEffect, useState } from "react";
import api from "../services/api";

function Movimientos() {

    const [movimientos, setMovimientos] = useState([]);


    async function cargarMovimientos() {

        try {

            const respuesta = await api.get("/transacciones/");

            setMovimientos(respuesta.data);

        } catch(error) {

            console.error(error);

            alert("No se pudieron cargar los movimientos");

        }

    }


    useEffect(() => {

        cargarMovimientos();

    }, []);


    return (

        <div className="container mt-4">

            <h2 className="mb-4">
                Historial de Movimientos
            </h2>


            <table className="table table-striped table-bordered shadow">

                <thead className="table-dark">

                    <tr>

                        <th>ID</th>
                        <th>Tipo</th>
                        <th>Monto</th>
                        <th>ID Socio</th>

                    </tr>

                </thead>


                <tbody>

                    {
                        movimientos.map((movimiento)=>(

                            <tr key={movimiento.id}>

                                <td>
                                    {movimiento.id}
                                </td>

                                <td>
                                    {movimiento.tipo}
                                </td>

                                <td>
                                    ${movimiento.monto}
                                </td>

                                <td>
                                    {movimiento.socio_id}
                                </td>

                            </tr>

                        ))
                    }

                </tbody>

            </table>


        </div>

    );

}

export default Movimientos;