"use client";

import React from "react";
import { motion } from "framer-motion";

import { STEPS } from "@/constants";
import { useAppSelector } from "@/store/hooks";
import StepIndicator from "@/components/ui/StepIndicator";

const ProgressIndicator = () => {
    const step = useAppSelector((state) => state.workflow.step);

    return (
        <motion.div
            className="mb-2 sm:mb-4 lg:mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, delay: 0.2 }}
            role="navigation"
            aria-label="Progress indicator"
        >
            <StepIndicator steps={STEPS} currentStep={step} />
        </motion.div>
    );
};

export default ProgressIndicator;
