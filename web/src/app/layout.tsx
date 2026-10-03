import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "AquaEye | Aquaculture Research Observatory",
  description: "Recorded underwater shrimp detection experiments, image enhancement, and spatial clustering with transparent research provenance.",
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
