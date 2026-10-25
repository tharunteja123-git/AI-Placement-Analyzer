"use client";

import { useCallback, useState } from "react";
import { useDropzone, type FileRejection } from "react-dropzone";
import { FileText, UploadCloud, X } from "lucide-react";

const MAX_BYTES = 5 * 1024 * 1024;

interface DropzoneProps {
  file: File | null;
  onChange: (file: File | null) => void;
}

function formatSize(bytes: number) {
  return bytes < 1024 * 1024
    ? `${Math.max(1, Math.round(bytes / 1024))} KB`
    : `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function Dropzone({ file, onChange }: DropzoneProps) {
  const [rejection, setRejection] = useState<string | null>(null);

  const onDrop = useCallback(
    (accepted: File[], rejected: FileRejection[]) => {
      if (rejected.length > 0) {
        const code = rejected[0].errors[0]?.code;
        setRejection(
          code === "file-too-large"
            ? "That file is over 5 MB. Upload a smaller resume."
            : "Upload a PDF, Word (.docx) or text file."
        );
        return;
      }
      setRejection(null);
      if (accepted[0]) onChange(accepted[0]);
    },
    [onChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    maxSize: MAX_BYTES,
    multiple: false,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
    },
  });

  if (file) {
    return (
      <div className="flex items-center gap-3 rounded-xl border border-line bg-white px-4 py-4">
        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-mint text-mint-ink">
          <FileText size={20} aria-hidden />
        </span>
        <div className="min-w-0 flex-1">
          <p className="truncate font-medium">{file.name}</p>
          <p className="text-sm text-slate">{formatSize(file.size)}</p>
        </div>
        <button
          type="button"
          onClick={() => onChange(null)}
          className="rounded-lg p-2 text-slate transition-colors hover:bg-paper hover:text-ink"
          aria-label={`Remove ${file.name}`}
        >
          <X size={18} aria-hidden />
        </button>
      </div>
    );
  }

  return (
    <div>
      <div
        {...getRootProps()}
        className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-12 text-center transition-colors ${
          isDragActive
            ? "border-ultramarine bg-ultramarine/5"
            : "border-line bg-white hover:border-ultramarine/60"
        }`}
      >
        <input {...getInputProps()} aria-label="Resume file" />
        <UploadCloud size={30} className="mb-3 text-ultramarine" aria-hidden />
        <p className="font-medium">
          {isDragActive ? "Drop your resume here" : "Drop your resume here, or click to browse"}
        </p>
        <p className="mt-1 text-sm text-slate">PDF, Word or text file, up to 5 MB</p>
      </div>
      {rejection && (
        <p role="alert" className="mt-2 text-sm text-rose-ink">
          {rejection}
        </p>
      )}
    </div>
  );
}