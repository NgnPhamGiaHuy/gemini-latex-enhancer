"use client";

import React, { useEffect } from "react";

import { setIsClient } from "@/store/slices/clientSlice";
import { useAppDispatch, useAppSelector } from "@/store/hooks";

import Main from "@/components/layouts/Main";
import Header from "@/components/layouts/Header";
import Wrapper from "@/components/layouts/Wrapper";
import FullScreenProgress from "@/components/ui/FullScreenProgress";
import ProgressIndicator from "@/components/features/ProgressIndicator";

const ResumeEnhancer = () => {
    const dispatch = useAppDispatch();
    const isClient = useAppSelector((state) => state.client.isClient);

    useEffect(() => {
        dispatch(setIsClient(true));
    }, []);

    if (!isClient) {
        return (
            <div
                className="flex items-center justify-center min-h-screen"
                role="status"
                aria-label="Loading application"
            >
                <div className="animate-spin h-8 w-8 border-2 border-foreground border-t-transparent" />
            </div>
        );
    }

    return (
        <Wrapper>
            <Header
                title={"Gemini LaTeX Enhancer"}
                description={"AI‑assisted CV enhancement with LaTeX outputs"}
            />
            <ProgressIndicator />
            <Main />
            {/* Full Screen Progress Overlay */}
            <FullScreenProgress />
        </Wrapper>
    );
};

export default ResumeEnhancer;
