import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HubHome from "../views/HubHome.jsx";
import DrafterWorkspace from "../views/DrafterWorkspace.jsx";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<HubHome />} />
      <Route path="/agents/drafter" element={<DrafterWorkspace />} />
    </Routes>
  </BrowserRouter>
);
