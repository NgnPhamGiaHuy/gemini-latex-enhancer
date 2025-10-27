"use client";

import { Brain } from "lucide-react";
import { motion } from "framer-motion";

import type { AIModel } from "@/libs/api";

interface SelectedModelInfoProps {
    model: AIModel;
}

const SelectedModelInfo = ({ model }: SelectedModelInfoProps) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="p-3 bg-white nb-border nb-shadow"
        >
            <div className="text-sm">
                <div className="font-medium mb-1 flex items-center gap-2">
                    <Brain className="h-4 w-4 text-primary" />
                    {model.name}
                </div>
                <div className="text-muted-foreground">{model.description}</div>
            </div>
        </motion.div>
    );
};

export default SelectedModelInfo;
