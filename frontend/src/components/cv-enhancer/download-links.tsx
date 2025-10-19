"use client";

import { motion } from "framer-motion";
import { FileText, Download } from "lucide-react";

import { buildOutputUrl } from "@/lib/api";

interface DownloadLinksProps {
    generateResult: {
        tex?: string;
        pdf?: string | null;
    };
}

const DownloadLinks = ({ generateResult }: DownloadLinksProps) => {
    return (
        <div className="grid gap-4">
            {generateResult.tex &&
            String(generateResult.tex).toLowerCase().endsWith(".zip") ? (
                <motion.a
                    href={buildOutputUrl(generateResult.tex)}
                    download
                    target="_blank"
                    className="flex items-center justify-between p-4 nb-border nb-shadow bg-white"
                    whileHover={{ x: -2, y: -2 }}
                >
                    <div className="flex items-center gap-3">
                        <FileText className="h-8 w-8 text-green-600" />
                        <div>
                            <p className="font-medium">Download All (ZIP)</p>
                            <p className="text-sm text-muted-foreground">
                                Batch enhanced results
                            </p>
                        </div>
                    </div>
                    <Download className="h-5 w-5" />
                </motion.a>
            ) : generateResult.tex ? (
                <motion.a
                    href={buildOutputUrl(generateResult.tex)}
                    download
                    target="_blank"
                    className="flex items-center justify-between p-4 nb-border nb-shadow bg-white"
                    whileHover={{ x: -2, y: -2 }}
                >
                    <div className="flex items-center gap-3">
                        <FileText className="h-8 w-8 text-blue-500" />
                        <div>
                            <p className="font-medium">LaTeX Source</p>
                            <p className="text-sm text-muted-foreground">
                                .tex file
                            </p>
                        </div>
                    </div>
                    <Download className="h-5 w-5" />
                </motion.a>
            ) : null}

            {/* Hide PDF section entirely if this is a batch (zip) download */}
            {!(
                generateResult.tex &&
                String(generateResult.tex).toLowerCase().endsWith(".zip")
            ) && generateResult.pdf ? (
                <>
                    <motion.a
                        href={buildOutputUrl(generateResult.pdf as string)}
                        download
                        target="_blank"
                        className="flex items-center justify-between p-4 nb-border nb-shadow bg-white"
                        whileHover={{ x: -2, y: -2 }}
                    >
                        <div className="flex items-center gap-3">
                            <FileText className="h-8 w-8 text-red-500" />
                            <div>
                                <p className="font-medium">PDF Document</p>
                                <p className="text-sm text-muted-foreground">
                                    Ready to print
                                </p>
                            </div>
                        </div>
                        <Download className="h-5 w-5" />
                    </motion.a>

                    <div className="mt-4">
                        <h3 className="text-lg font-bold uppercase mb-2">
                            PDF Preview
                        </h3>
                        <div className="nb-border nb-shadow bg-white overflow-hidden">
                            <iframe
                                src={buildOutputUrl(
                                    generateResult.pdf as string
                                )}
                                className="w-full h-224"
                                title="CV Preview"
                            />
                        </div>
                    </div>
                </>
            ) : !(
                  generateResult.tex &&
                  String(generateResult.tex).toLowerCase().endsWith(".zip")
              ) ? (
                <div className="p-4 nb-border nb-shadow bg-white">
                    <div className="flex items-center gap-3">
                        <FileText className="h-8 w-8 text-muted-foreground" />
                        <div>
                            <p className="font-bold uppercase text-foreground">
                                PDF Generation Failed
                            </p>
                            <p className="text-sm text-muted-foreground">
                                LaTeX compilation failed - download .tex file
                                and compile locally
                            </p>
                        </div>
                    </div>
                </div>
            ) : null}
        </div>
    );
};

export default DownloadLinks;
