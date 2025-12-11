
import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Wine, Database, FileBarChart } from 'lucide-react';

export default function LandingPage() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="max-w-3xl"
            >
                <div className="mb-6 flex justify-center">
                    <div className="w-24 h-24 rounded-full bg-burgundy/10 flex items-center justify-center border-2 border-gold/30">
                        <Wine className="w-12 h-12 text-burgundy" />
                    </div>
                </div>

                <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-gold to-yellow-600">
                    VinoVeritas
                </h1>
                <p className="text-xl text-gray-400 mb-10 leading-relaxed">
                    The intersection of rigorous data science and the art of winemaking.
                    <br />Predict wine quality with precision using our advanced machine learning models.
                </p>

                <div className="flex flex-wrap gap-4 justify-center">
                    <Link to="/predict" className="btn-primary flex items-center gap-2 text-lg px-8 py-3">
                        Start Assessment <ArrowRight className="w-5 h-5" />
                    </Link>
                    <Link to="/dashboard" className="px-8 py-3 rounded-lg border border-gray-600 hover:border-gold hover:text-gold transition-colors text-gray-300">
                        View Analytics
                    </Link>
                </div>
            </motion.div>

            <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
                <FeatureCard
                    icon={Wine}
                    title="Quality Prediction"
                    desc="Instant analysis of physicochemical properties to estimate wine grade."
                />
                <FeatureCard
                    icon={Database}
                    title="Data Exploration"
                    desc="Deep dive into dataset correlations and feature distributions."
                />
                <FeatureCard
                    icon={FileBarChart}
                    title="Automated Reporting"
                    desc="Generate and view comprehensive PDF-style reports on the fly."
                />
            </div>
        </div>
    );
}

function FeatureCard({ icon: Icon, title, desc }) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="bg-dark-card p-6 rounded-xl border border-gray-800 hover:border-gold/30 transition-all"
        >
            <Icon className="w-10 h-10 text-burgundy mb-4" />
            <h3 className="text-xl font-serif text-gold mb-2">{title}</h3>
            <p className="text-gray-400 text-sm">{desc}</p>
        </motion.div>
    );
}
