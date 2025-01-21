import React, { useEffect, useState } from "react";
import axios from "axios";
import AddRepositoryForm from "./AddRepositoryForm";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface Repository {
  id: number;
  name: string;
  description: string;
  url: string;
}

const App: React.FC = () => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(5); // Repositories per page
  const [totalRepositories, setTotalRepositories] = useState(0);

  const [editingRepo, setEditingRepo] = useState<Repository | null>(null);

  useEffect(() => {
    const fetchRepositories = async () => {
      setLoading(true);
      setError(null); // Reset error state
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/repositories/?skip=${(currentPage - 1) * pageSize}&limit=${pageSize}`
        );
        setRepositories(response.data.repositories);
        setTotalRepositories(response.data.total);
      } catch (error) {
        setError("Failed to fetch repositories. Please try again.");
        toast.error("Failed to fetch repositories.");
      } finally {
        setLoading(false);
      }
    };

    fetchRepositories();
  }, [currentPage, pageSize]);

  const handleRepositoryAdded = (newRepo: Repository) => {
    setRepositories((prev) => [newRepo, ...prev]);
    setTotalRepositories((prev) => prev + 1);
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/repositories/${id}/`);
      setRepositories((prev) => prev.filter((repo) => repo.id !== id));
      setTotalRepositories((prev) => prev - 1);
      toast.success("Repository deleted successfully!");
    } catch {
      toast.error("Failed to delete repository. Please try again.");
    }
  };

  const handleEdit = (repo: Repository) => {
    setEditingRepo(repo); // Set the current repository for editing
  };

  const handleSaveEdit = async (updatedRepo: Repository) => {
    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/repositories/${updatedRepo.id}/`,
        updatedRepo
      );
      setRepositories((prev) =>
        prev.map((repo) => (repo.id === updatedRepo.id ? response.data : repo))
      );
      toast.success("Repository updated successfully!");
      setEditingRepo(null); // Exit edit mode
    } catch {
      toast.error("Failed to update repository. Please try again.");
    }
  };

  const handleCancelEdit = () => {
    setEditingRepo(null); // Exit edit mode
  };

  return (
    <div className="p-8">
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      <header className="text-center mb-8">
        <h1 className="bg-blue-500 text-white text-2xl sm:text-3xl font-bold py-4 rounded">
          Welcome to CodeSense Frontend
        </h1>
      </header>
      <main className="max-w-4xl mx-auto">
        <AddRepositoryForm onRepositoryAdded={handleRepositoryAdded} />
        <h2 className="text-xl font-semibold mt-8 mb-4">Repositories</h2>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <>
            <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {repositories.map((repo) =>
                editingRepo && editingRepo.id === repo.id ? (
                  <li
                    key={repo.id}
                    className="p-4 border rounded shadow hover:shadow-lg"
                  >
                    <div className="mb-2">
                      <label className="block text-sm font-medium">Name:</label>
                      <input
                        type="text"
                        value={editingRepo.name}
                        onChange={(e) =>
                          setEditingRepo({
                            ...editingRepo,
                            name: e.target.value,
                          })
                        }
                        className="w-full p-2 border rounded"
                      />
                    </div>
                    <div className="mb-2">
                      <label className="block text-sm font-medium">
                        Description:
                      </label>
                      <input
                        type="text"
                        value={editingRepo.description}
                        onChange={(e) =>
                          setEditingRepo({
                            ...editingRepo,
                            description: e.target.value,
                          })
                        }
                        className="w-full p-2 border rounded"
                      />
                    </div>
                    <div className="mb-2">
                      <label className="block text-sm font-medium">URL:</label>
                      <input
                        type="text"
                        value={editingRepo.url}
                        onChange={(e) =>
                          setEditingRepo({
                            ...editingRepo,
                            url: e.target.value,
                          })
                        }
                        className="w-full p-2 border rounded"
                      />
                    </div>
                    <div className="flex justify-end">
                      <button
                        onClick={() => handleSaveEdit(editingRepo)}
                        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mr-2"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                      >
                        Cancel
                      </button>
                    </div>
                  </li>
                ) : (
                  <li
                    key={repo.id}
                    className="p-4 border rounded shadow hover:shadow-lg"
                  >
                    <h3 className="text-lg font-bold">{repo.name}</h3>
                    <p>{repo.description}</p>
                    <a
                      href={repo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:text-blue-700"
                    >
                      Visit Repository
                    </a>
                    <div className="flex justify-between mt-2">
                      <button
                        onClick={() => handleEdit(repo)}
                        className="text-green-500 hover:text-green-700"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(repo.id)}
                        className="text-red-500 hover:text-red-700 ml-4"
                      >
                        Delete
                      </button>
                    </div>
                  </li>
                )
              )}
            </ul>
            <div className="flex justify-between mt-4">
              <button
                onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <span>Page {currentPage}</span>
              <button
                onClick={() =>
                  setCurrentPage((prev) =>
                    Math.min(prev + 1, Math.ceil(totalRepositories / pageSize))
                  )
                }
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                disabled={currentPage === Math.ceil(totalRepositories / pageSize)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  );
};

export default App;
