"use client";

import React from "react";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

interface HeaderProps {
    title: string;
    description: string;
}

const Header: React.FC<HeaderProps> = ({ title, description }) => {
    return (
        <motion.header
            className={
                "mb-2 sm:mb-4 lg:mb-8 flex flex-col items-center justify-center text-center"
            }
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75 }}
            role="banner"
        >
            <div className="mb-2 sm:mb-4 px-4 py-2 inline-flex items-center justify-center gap-2 sm:gap-3 bg-white nb-border nb-shadow">
                <Sparkles
                    className="size-6 sm:size-8 text-foreground"
                    aria-hidden="true"
                />
                <h1 className="text-2xl sm:text-3xl lg:text-4xl text-foreground font-bold uppercase tracking-tight">
                    {title}
                </h1>
            </div>
            <p className="mt-2 px-4 py-1 inline-block bg-secondary text-xs sm:text-sm lg:text-base text-secondary-foreground nb-border nb-shadow">
                {description}
            </p>
        </motion.header>
    );
};

export default Header;
