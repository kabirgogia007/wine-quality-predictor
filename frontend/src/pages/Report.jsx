
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { FileText, Download } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function ReportDocs() {
    const [report, setReport] = useState('# Loading Report...');
    const [error, setError] = useState(false);

    useEffect(() => {
        const fetchReport = async () => {
            try {
                const res = await axios.get(`${API_URL}/report`);
                setReport(res.data.content);
            } catch (err) {
                setReport("# Error Loading Report\nCould not fetch the project report from backend.");
                setError(true);
            }
        };
        fetchReport();
    }, []);

    return (
        <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-gray-700">
                <div className="flex items-center gap-3">
                    <div className="p-3 bg-burgundy rounded-lg">
                        <FileText className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold text-white">Project Report</h1>
                        <p className="text-gray-400 text-sm">Generated Documentation & Metrics</p>
                    </div>
                </div>
                <button
                    onClick={() => window.print()}
                    className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-md text-sm transition-colors"
                >
                    <Download className="w-4 h-4" /> Print / Save PDF
                </button>
            </div>

            <div className="bg-white text-gray-900 p-8 md:p-12 rounded-lg shadow-2xl prose prose-slate max-w-none prose-headings:font-serif prose-headings:text-burgundy prose-code:text-burgundy">
                <ReactMarkdown
                    components={{
                        img: ({ node, ...props }) => {
                            // If the image source is relative (eda_*.png), prepend API URL
                            // The backend report has ![alt](eda_histograms.png)
                            let src = props.src;
                            if (!src.startsWith('http')) {
                                src = `${API_URL}/eda/${src}`;
                            }
                            return <img {...props} src={src} className="rounded-lg shadow-md border border-gray-200 mx-auto my-4" />;
                        }
                    }}
                >
                    {report}
                </ReactMarkdown>
            </div>
        </div>
    );
}
