import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import GeneralPanel from "./main_panels/general_panel.jsx";
import AppFooter from "./footer/footer.jsx";
import AppHeader from "./header/header.jsx";
import Login from "./header/login.jsx";
import Logout from "./header/logout.jsx";
import CarTable from "./tables/unauth_car_table.jsx";
import GeneralManual from "./tables/manual.jsx";
import AuthCarDetail from "./tables/auth_car_detail.jsx";
import AuthCarTable from "./tables/auth_car_table.jsx";
import AuthRepairTable from "./tables/auth_repair_table.jsx";
import AuthMaitenanceTable from "./tables/auth_maitenance_table.jsx";
import Company from "./tables/company.jsx";
import "./styles.css";

const App = () => {
  return (
    <div className="App">
      <Router>
        <AppHeader />
        <Routes>
          <Route path="/login" element={<Login />} exact />
          <Route path="/logout" element={<Logout />} exact />
          <Route path="/" element={<GeneralPanel />} exact />
          <Route path="/company/:id" element={<Company />} exact />
          <Route path="/car/:id" element={<CarTable />} exact />
          <Route path="/cars/:id" element={<AuthCarDetail />} />
          <Route path="/manual/:id" element={<GeneralManual />} />
          <Route path="/maitenance" element={<AuthMaitenanceTable />} />
          <Route path="/repair" element={<AuthRepairTable />} />
        </Routes>
        <AppFooter />
      </Router>
    </div>
  );
};

export default App;
