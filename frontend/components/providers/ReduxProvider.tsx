"use client";

import React from "react";
import { Provider } from "react-redux";
import { AppTooltipProvider } from "@/components/ui/Tooltip";
import { store } from "@/store";

interface ReduxProviderProps {
    children: React.ReactNode;
}

const ReduxProvider: React.FC<ReduxProviderProps> = ({ children }) => {
    return (
        <Provider store={store}>
            <AppTooltipProvider>{children}</AppTooltipProvider>
        </Provider>
    );
};

export default ReduxProvider;
