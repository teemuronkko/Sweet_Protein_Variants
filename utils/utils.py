def get_sequence_from_pdb_fasta(pdb_id, chain_id):
    '''
    Function to get a fasta sequence from RCSB PDB using the PDB identifier and the chain ID
    '''
    from Bio import SeqIO
    import requests
    from io import StringIO

    # Link to the fasta file on RCSB PDB
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}/display"
    fasta = requests.get(url).text

    # Return the requested sequence - try first the author chain ID, then the PDB chain ID
    # Iterator to read fasta sequences from the file
    fasta_iterator = SeqIO.parse(StringIO(fasta), "fasta")
    for seq in fasta_iterator:
        if f"[auth {chain_id}]" in seq.description:
            return seq.seq

    fasta_iterator = SeqIO.parse(StringIO(fasta), "fasta")
    for seq in fasta_iterator:
        if f"Chain {chain_id}" in seq.description:
            return seq.seq

