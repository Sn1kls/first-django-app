import { WebSocketProvider } from "./WebSocketContext";

import "./App.css";

function App() {
    return (
        <WebSocketProvider>
            <div className="w-100 h-100">HELLO</div>
        </WebSocketProvider>
    );
}

export default App;
