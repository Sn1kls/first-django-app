import React, { createContext, useContext, useEffect } from "react";
import useWebSocket from "react-use-websocket";

const WebSocketContext = createContext();

export const WebSocketProvider = ({ children }) => {
    const { sendJsonMessage, lastJsonMessage } = useWebSocket(`ws://localhost:8000/ws/notifications/`);

    useEffect(() => {
        console.log("lastJsonMessage", lastJsonMessage);
    }, [lastJsonMessage]);

    useEffect(() => {
        sendJsonMessage({
            action: "subscribe",
            user: "1",
            token: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNTk3MjMwLCJpYXQiOjE3MzM1MTA4MzAsImp0aSI6IjQ0MTRiNWE4NTBmMDRmZGQ4MTc1ZDc2YThkOTE5NzVmIiwidXNlcl9pZCI6MX0.wp1rBDP68k62R_XOEFC76G24wC0IqdZV6-OGRixr8Jo",
        });
    }, []);

    const value = {
        sendJsonMessage,
        lastJsonMessage,
    };

    return <WebSocketContext.Provider value={value}>{children}</WebSocketContext.Provider>;
};

export const useWebSocketContext = () => {
    return useContext(WebSocketContext);
};
