import React, { createContext, useContext, useEffect } from "react";
import useWebSocket from "react-use-websocket";

const WebSocketContext = createContext();

export const WebSocketProvider = ({ children }) => {
    const { sendJsonMessage, lastJsonMessage } = useWebSocket(`ws://localhost:8000/ws/notifications/?Authorization=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NTk3MTY0LCJpYXQiOjE3MzQ1MTA3NjQsImp0aSI6ImQ4M2UwYTJiZmQ1NjRiNThiODFmNTY3ZWM4OTRhNzFjIiwidXNlcl9pZCI6MX0.GYCz0_ekYFNH6-HTXhFHG_zzsJMlXugCWvvAacII9pE`);

    useEffect(() => {
        console.log("lastJsonMessage", lastJsonMessage);
    }, [lastJsonMessage]);

    useEffect(() => {
        sendJsonMessage({
            action: "subscribe",
            user: "1",
            token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NTk3MTY0LCJpYXQiOjE3MzQ1MTA3NjQsImp0aSI6ImQ4M2UwYTJiZmQ1NjRiNThiODFmNTY3ZWM4OTRhNzFjIiwidXNlcl9pZCI6MX0.GYCz0_ekYFNH6-HTXhFHG_zzsJMlXugCWvvAacII9pE",
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
