const request = require('supertest');
const app = require('./app');
const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');

jest.mock('pdf-parse', () => jest.fn());
jest.mock('mammoth');

describe('CV Extraction Service', () => {
  it('should reject requests without a file', async () => {
    const res = await request(app).post('/extract');
    expect(res.statusCode).toEqual(400);
    expect(res.body.error).toEqual('No file provided.');
  });

  it('should reject files that are not PDF or DOCX', async () => {
    const res = await request(app)
      .post('/extract')
      .attach('cv', Buffer.from('dummy text'), 'test.txt');
    expect(res.statusCode).toEqual(400);
    expect(res.body.error).toEqual('Invalid file type. Only PDF and DOCX are allowed.');
  });

  it('should extract text from a PDF file', async () => {
    pdfParse.mockResolvedValue({ text: 'Extracted PDF text' });

    const res = await request(app)
      .post('/extract')
      .attach('cv', Buffer.from('dummy pdf'), {
        filename: 'test.pdf',
        contentType: 'application/pdf',
      });

    expect(res.statusCode).toEqual(200);
    expect(res.body.text).toEqual('Extracted PDF text');
    expect(pdfParse).toHaveBeenCalled();
  });

  it('should extract text from a DOCX file', async () => {
    mammoth.extractRawText.mockResolvedValue({ value: 'Extracted DOCX text' });

    const res = await request(app)
      .post('/extract')
      .attach('cv', Buffer.from('dummy docx'), {
        filename: 'test.docx',
        contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      });

    expect(res.statusCode).toEqual(200);
    expect(res.body.text).toEqual('Extracted DOCX text');
    expect(mammoth.extractRawText).toHaveBeenCalled();
  });

  it('should save a candidate profile', async () => {
    const profile = {
      name: 'John Doe',
      email: 'john@example.com',
      skills: ['React', 'Node.js'],
      education: ['BSc CS'],
      experience: ['Developer']
    };

    const res = await request(app)
      .post('/profile')
      .send(profile);

    expect(res.statusCode).toEqual(201);
    expect(res.body.message).toEqual('Profile saved successfully');
    expect(res.body.profile.id).toBeDefined();
    expect(res.body.profile.name).toEqual('John Doe');
  });

  it('should reject a profile without name and email', async () => {
    const profile = {
      skills: ['React']
    };

    const res = await request(app)
      .post('/profile')
      .send(profile);

    expect(res.statusCode).toEqual(400);
    expect(res.body.error).toEqual('Profile must have at least a name or email');
  });
});
