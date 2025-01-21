import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";

interface AddRepositoryFormProps {
  onRepositoryAdded: (newRepo: any) => void; // Notify parent component
}

const AddRepositoryForm: React.FC<AddRepositoryFormProps> = ({
  onRepositoryAdded,
}) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [url, setUrl] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/repositories/", {
        name,
        description,
        url,
      });
      toast.success("Repository added successfully!");
      onRepositoryAdded(response.data); // Pass the new repository to parent
      setName("");
      setDescription("");
      setUrl("");
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        toast.error(error.response.data.detail || "Repository already exists.");
      } else {
        toast.error("Failed to add repository. Please try again.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 p-4 border rounded shadow">
      <h2 className="text-lg font-semibold mb-4">Add a New Repository</h2>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Description:</label>
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">URL:</label>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <button
        type="submit"
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Add Repository
      </button>
    </form>
  );
};

export default AddRepositoryForm;
