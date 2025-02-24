import { Routes, Route } from "react-router-dom";

import Header from "./components/layout/header";
import TemplateAction from "./pages/TemplateAction";
import Analytic from "./pages/Analytic";

const App = () => {
    return (<>
        <Header />
        <Routes>
            <Route path="/" element={<TemplateAction />} />
            <Route path="/analytic" element={<Analytic />} />
        </Routes>
        {/* <TemplateAction /> */}
    </>)
}

export default App;