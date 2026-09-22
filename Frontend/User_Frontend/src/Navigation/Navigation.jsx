import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../Pages/Home.jsx";
import Login from "../Pages/Login.jsx";
import Registration from "../Pages/Registration.jsx";
function Navigation() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/registration" element={<Registration />} />
            </Routes>
        </BrowserRouter>
    );
}
export default Navigation;