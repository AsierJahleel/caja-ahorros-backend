import { useState } from "react";
import api from "../services/api";

function Inicio() {

    const [nombre, setNombre] = useState("");
    const [cedula, setCedula] = useState("");
    const [saldo, setSaldo] = useState("");
    const [mensaje, setMensaje] = useState("");

    async function guardarSocio() {

        if (!nombre || !cedula || !saldo) {
            setMensaje("Todos los campos son obligatorios.");
            return;
        }

        if (Number(saldo) < 0) {
            setMensaje("El saldo no puede ser negativo.");
            return;
        }

        try {

            await api.post("/socios/", {
                nombre,
                cedula,
                saldo: Number(saldo)
            });

            setMensaje("Socio registrado correctamente");

            setNombre("");
            setCedula("");
            setSaldo("");

        } catch(error) {

            console.error(error);
            alert("No se pudo registrar el socio");

        }
    }


    return (
        <div className="container mt-4">

            <h1 className="text-center mb-4">
                Sistema Caja de Ahorros
            </h1>


            <div className="row">

                <div className="col-md-4">

                    <div className="card shadow">

                        <div className="card-body">

                            <h5 className="card-title">
                                👥 Socios
                            </h5>

                            <p>
                                Registro de nuevos socios.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="col-md-4">

                    <div className="card shadow">

                        <div className="card-body">

                            <h5 className="card-title">
                                💰 Ahorros
                            </h5>

                            <p>
                                Administración de saldos.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="col-md-4">

                    <div className="card shadow">

                        <div className="card-body">

                            <h5 className="card-title">
                                🔄 Transacciones
                            </h5>

                            <p>
                                Depósitos y retiros.
                            </p>

                        </div>

                    </div>

                </div>

            </div>


            <hr className="my-4"/>


            <h2>
                Registrar Socio
            </h2>


            {
                mensaje && (
                    <div className="alert alert-success">
                        {mensaje}
                    </div>
                )
            }


            <div className="card shadow">

                <div className="card-body">


                    <input
                        className="form-control mb-3"
                        placeholder="Nombre"
                        value={nombre}
                        onChange={(e)=>setNombre(e.target.value)}
                    />


                    <input
                        className="form-control mb-3"
                        placeholder="Cédula"
                        value={cedula}
                        onChange={(e)=>setCedula(e.target.value)}
                    />


                    <input
                        className="form-control mb-3"
                        type="number"
                        placeholder="Saldo inicial"
                        value={saldo}
                        onChange={(e)=>setSaldo(e.target.value)}
                    />


                    <button
                        className="btn btn-primary"
                        onClick={guardarSocio}
                    >
                        Guardar Socio
                    </button>


                </div>

            </div>


        </div>

    );

}

export default Inicio;