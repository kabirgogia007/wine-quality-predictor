
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BarChart2, Maximize2 } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function Dashboard() {
    const images = [
        { id: 'eda_histograms.png', title: 'Feature Histograms', desc: 'Distribution of input variables across the dataset.' },
        { id: 'eda_correlation.png', title: 'Correlation Matrix', desc: 'Heatmap showing relationships between wine properties.' },
        { id: 'eda_quality_dist.png', title: 'Quality Distribution', desc: 'The spread of wine quality ratings in the training set.' },
    ];

    const [selectedImage, setSelectedImage] = useState(null);

    return (
        <div className="space-y-8">
            <div className="flex items-center gap-4 mb-8">
                <BarChart2 className="w-8 h-8 text-gold" />
                <h2 className="text-3xl font-serif text-white">Data Analytics Dashboard</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {images.map((img) => (
                    <motion.div
                        key={img.id}
                        whileHover={{ y: -5 }}
                        className="group relative bg-dark-card rounded-xl overflow-hidden shadow-xl border border-gray-800 hover:border-gold/50 transition-all cursor-pointer"
                        onClick={() => setSelectedImage(img)}
                    >
                        <div className="aspect-video bg-gray-900 border-b border-gray-800 overflow-hidden relative">
                            {/* Use direct IMG tag pointing to backend endpoint */}
                            <img
                                src={`${API_URL}/eda/${img.id}`}
                                alt={img.title}
                                className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity"
                                onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.src = "https://via.placeholder.com/600x400/2b2b2b/808080?text=Plot+Not+Generated";
                                }}
                            />
                            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                                <Maximize2 className="text-white w-8 h-8" />
                            </div>
                        </div>
                        <div className="p-4">
                            <h3 className="text-lg font-bold text-gray-200 mb-1">{img.title}</h3>
                            <p className="text-sm text-gray-400">{img.desc}</p>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Lightbox */}
            {selectedImage && (
                <div
                    className="fixed inset-0 z-[100] bg-black/90 backdrop-blur-sm flex items-center justify-center p-4 md:p-10"
                    onClick={() => setSelectedImage(null)}
                >
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="relative max-w-7xl w-full max-h-full overflow-auto bg-dark-card rounded-lg p-2"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            className="absolute top-4 right-4 bg-black/50 hover:bg-burgundy text-white p-2 rounded-full transition-colors"
                            onClick={() => setSelectedImage(null)}
                        >
                            <Maximize2 className="w-6 h-6 rotate-45" /> {/* Close icon hack */}
                        </button>
                        <img
                            src={`${API_URL}/eda/${selectedImage.id}`}
                            alt={selectedImage.title}
                            className="w-full h-auto rounded"
                        />
                        <div className="p-4 text-center">
                            <h3 className="text-2xl font-serif text-gold">{selectedImage.title}</h3>
                        </div>
                    </motion.div>
                </div>
            )}
        </div>
    );
}
