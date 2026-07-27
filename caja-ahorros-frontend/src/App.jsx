import { Routes, Route, Link } from "react-router-dom";

import Inicio from "./pages/Inicio";
import Saldo from "./pages/Saldo";
import Movimientos from "./pages/Movimientos";
import Transacciones from "./pages/Transacciones";

function App() {
  return (
    <div>

      <header
        style={{
          background: "#1976d2",
          padding: "20px",
          color: "white",
        }}
      >
        <h1>Caja de Ahorros</h1>

        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
    
    <div className="container">

        <a className="navbar-brand" href="/">
            Caja de Ahorros
        </a>


        <div className="navbar-nav">

            <a className="nav-link" href="/">
                Inicio
            </a>

            <a className="nav-link" href="/saldo">
                Saldo
            </a>

            <a className="nav-link" href="/movimientos">
                Movimientos
            </a>

            <a className="nav-link" href="/transacciones">
                Transacciones
            </a>

        </div>

    </div>

</nav>
        
      </header>
      

      <main style={{ padding: "20px" }}>

        <Routes>

          <Route path="/" element={<Inicio />} />

          <Route path="/saldo" element={<Saldo />} />

          <Route path="/movimientos" element={<Movimientos />} />

          <Route path="/transacciones" element={<Transacciones />} />

        </Routes>

      </main>

    </div>
  );
}

export default App;