"use client";

import { motion } from "framer-motion";

import { useAppSelector } from "@/store/hooks";

import JobDetailsForm from "@/components/features/JobDetailsForm";

const AlignStep = () => {
    const step = useAppSelector((state) => state.workflow.step);

    if (step !== "align") return null;

    return (
        <motion.div
            key="align"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.4 }}
        >
            <div className="max-w-2xl mx-auto px-3 sm:px-0">
                <JobDetailsForm loading={false} />
            </div>
        </motion.div>
    );
};

export default AlignStep;
