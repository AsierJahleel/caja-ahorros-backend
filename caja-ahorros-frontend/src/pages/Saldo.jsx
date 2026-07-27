import { useEffect, useState } from "react";
import api from "../services/api";

function Saldo() {

    const [socios, setSocios] = useState([]);

    async function cargarSocios() {

        try {

            const respuesta = await api.get("/socios/");

            setSocios(respuesta.data);

        } catch(error) {

            console.error(error);

            alert("No se pudieron cargar los socios");

        }

    }


    useEffect(() => {

        cargarSocios();

    }, []);


    return (

        <div className="container mt-4">

            <h2 className="mb-4">
                Consulta de Saldos
            </h2>


            <table className="table table-bordered shadow">

                <thead className="table-dark">

                    <tr>

                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Cédula</th>
                        <th>Saldo</th>

                    </tr>

                </thead>


                <tbody>

                    {
                        socios.map((socio)=>(

                            <tr key={socio.id}>

                                <td>{socio.id}</td>

                                <td>{socio.nombre}</td>

                                <td>{socio.cedula}</td>

                                <td>
                                    ${socio.saldo}
                                </td>

                            </tr>

                        ))
                    }

                </tbody>

            </table>


        </div>

    );

}

export default Saldo;