import { useState } from "react";
import api from "../services/api";

function Transacciones() {

    const [tipo, setTipo] = useState("deposito");
    const [monto, setMonto] = useState("");
    const [socioId, setSocioId] = useState("");
    const [mensaje, setMensaje] = useState("");

    async function registrarTransaccion() {

        if (!monto || !socioId) {
            setMensaje("Complete todos los campos.");
            return;
        }

        if (Number(monto) <= 0) {
            setMensaje("El monto debe ser mayor a cero.");
            return;
        }

        try {

            await api.post("/transacciones/", null, {
                params: {
                    tipo: tipo,
                    monto: Number(monto),
                    socio_id: Number(socioId)
                }
            });

            setMensaje("Transacción realizada correctamente.");

            setMonto("");
            setSocioId("");

        } catch(error) {

            console.error(error);

            setMensaje("No se pudo realizar la transacción.");

        }

    }


    return (

        <div>

            <h2>Registrar Transacción</h2>

            {
 mensaje && (
    <div className="alert alert-success">
        {mensaje}
    </div>
 )
}


            <label>Tipo</label>
            <br />

            <select 
                value={tipo}
                onChange={(e)=>setTipo(e.target.value)}
            >

                <option value="deposito">
                    Depósito
                </option>

                <option value="retiro">
                    Retiro
                </option>

            </select>


            <br /><br />


            <label>Monto</label>
            <br />

            <input
                type="number"
                value={monto}
                onChange={(e)=>setMonto(e.target.value)}
            />


            <br /><br />


            <label>ID del Socio</label>
            <br />

            <input
                type="number"
                value={socioId}
                onChange={(e)=>setSocioId(e.target.value)}
            />


            <br /><br />


            <button onClick={registrarTransaccion}>
                Registrar
            </button>


        </div>

    );

}

export default Transacciones;